from datetime import date, datetime, timedelta
import csv
import json

from pathlib import Path
from flask import current_app, render_template
from flask_mail import Message

from backend.celery_app import celery
from backend.database import db
from backend.model import Availability, Trek, Booking, User


@celery.task(name="backend.tasks.update_trek_progress")
def update_trek_progress():
    today = date.today()

    updated_schedules = 0
    completed_schedules = 0
    completed_bookings = 0

    try:
        schedules = Availability.query.all()

        for schedule in schedules:
            trek = Trek.query.get(schedule.trek_id)

            if not trek:
                continue

            old_progress = schedule.progress_status
            old_status = schedule.status

            # 1. Trek has not started.
            if today < schedule.start_date:
                schedule.progress_status = "Not Started"

                # Do not override a staff member's manual
                # Open/Closed choice unless opening is invalid.
                if (
                    trek.status != "Active"
                    or schedule.avail_slot <= 0
                ):
                    schedule.status = "Closed"

            # 2. Trek has started but has not reached its end date.
            elif today < schedule.end_date:
                schedule.progress_status = "Ongoing"
                schedule.status = "Closed"

            # 3. End date reached: trek is completed.
            else:
                schedule.progress_status = "Completed"
                schedule.status = "Closed"

                # Mark active bookings as completed.
                count = Booking.query.filter(
                    Booking.availability_id == schedule.id,
                    Booking.status == "Booked"
                ).update(
                    {"status": "Completed"},
                    synchronize_session=False
                )

                completed_bookings += count

                if old_progress != "Completed":
                    completed_schedules += 1

            if (
                old_progress != schedule.progress_status
                or old_status != schedule.status
            ):
                updated_schedules += 1

        db.session.commit()

        return {
            "message": "Trek progress update completed.",
            "date": today.isoformat(),
            "updated_schedules": updated_schedules,
            "completed_schedules": completed_schedules,
            "completed_bookings": completed_bookings
        }

    except Exception:
        db.session.rollback()
        raise


@celery.task(name="backend.tasks.send_trek_reminders")
def send_trek_reminders():
    """    
    Find trekking schedules starting tomorrow.    
    Email delivery will be connected after checking your existing User and Flask-Mail configurations.
    """
    from flask_mail import Mail

    tomorrow = date.today() + timedelta(days=1)
    mail = Mail(current_app._get_current_object())

    sent_count = 0
    skipped_count = 0
    upcoming_treks = []

    schedules = Availability.query.all()

    for schedule in schedules:
        start_date = schedule.start_date

        if isinstance(start_date, str):
            try:
                start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
            except ValueError:
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                except ValueError:
                    current_app.logger.warning(
                        "Invalid start date for schedule %s", schedule.id,
                    )
                    continue

        if start_date != tomorrow:
            continue

        trek = db.session.get(Trek, schedule.trek_id)
        if not trek:
            continue

        upcoming_treks.append({
            "schedule_id": schedule.id,
            "trek_id": trek.id,
            "trek_name": trek.trek_name,
            "start_date": tomorrow.strftime("%d-%m-%Y"),
        })

        bookings = Booking.query.filter_by(availability_id=schedule.id, status="Booked").all()

        for booking in bookings:
            user = db.session.get(User, booking.usr_id)

            if not user or not user.email:
                skipped_count += 1
                current_app.logger.warning("Skipping reminder: missing user or email for booking %s", booking.id,)
                continue

            subject = (f"Reminder: Your trek '{trek.trek_name}' starts tomorrow.")
            body = (
                f"Hi {user.fullname},\n\n"
                "This is a reminder that your trek is scheduled for tomorrow.\n\n"
                f"Trek Name: {trek.trek_name}\n\n"
                f"Start Date: {tomorrow.strftime('%d-%m-%Y')}\n"
                f"End Date: {schedule.end_date.strftime('%d-%m-%Y')}\n\n"
                f"Location: {trek.location}\n"
                "Please prepare for your upcoming trek.\n\n"
                "Regards,\n"
                "Aggarwal HikeHorizon"
            )

            try:
                message = Message(
                    subject=subject,
                    recipients=[user.email],
                    body=body,
                )
                mail.send(message)
                sent_count += 1
                current_app.logger.info("Trek reminder sent for booking %s ", booking.id,)

            except Exception:
                skipped_count += 1
                current_app.logger.exception("Failed to send trek reminder for booking %s", booking.id,)


    current_app.logger.info(
        "Found %s trekking schdules starting tomorrow", len(upcoming_treks),
    )

    return {
        "message": "Daily trek reminder task completed.",
        "date": tomorrow.strftime("%d-%m-%Y"),
        "upcoming_treks": upcoming_treks,
        "emails_sent": sent_count,
        "emails_skipped": skipped_count
    }


@celery.task(name="backend.tasks.generate_monthly_report")
def generate_monthly_report(year=None, month=None):
    """Generate a monthly trekking activity report as HTML."""

    today = date.today()

    # When run by celery beat on the first day, generate the report for the prev month.
    if year is None and month is None:
        previous_month = today.replace(day=1) - timedelta(days=1)
        year = previous_month.year
        month = previous_month.month

    year = int(year)
    month = int(month)
    first_day = date(year, month, 1)

    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    schedules = Availability.query.all()
    monthly_schedules = []

    for schedule in schedules:
        start_date = schedule.start_date

        if isinstance(start_date, str):
            try:
                start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
            except ValueError:
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                except ValueError:
                    current_app.logger.warning(
                        "Invalid start date for schedule %s", schedule.id,
                    )
                    continue

        if (start_date and first_day <= start_date < next_month):
            monthly_schedules.append(schedule)

    trek_counts = {}
    participant_count = 0

    for schedule in monthly_schedules:
        trek = db.session.get(Trek, schedule.trek_id)

        if not trek:
            continue

        trek_counts[trek.trek_name] = (
            trek_counts.get(trek.trek_name, 0) + 1
        )

        bookings = Booking.query.filter_by(availability_id=schedule.id).all()

        participant_count += sum(
            1 for booking in bookings
            if booking.status in ("Booked", "Completed")
        )

    popular_treks = sorted(
        trek_counts.items(), key=lambda x: x[1], reverse=True
    )[:5]

    report_data = {
        "year": year,
        "month_name": first_day.strftime("%B"),
        "treks_conducted": sum(
            1 for schedule in monthly_schedules if schedule.progress_status == "Completed"
        ),
        "participants": participant_count,
        "popular_treks": popular_treks,
        "generated_at": datetime.now().strftime("%d-%m-%Y %H:%M"),
    }

    report_html = render_template("monthly_report.html", report=report_data)

    report_dir = Path(current_app.root_path) / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = (report_dir / f"monthly_report_{year}_{month:02d}.html")
    report_file.write_text(report_html, encoding="utf-8")

    return {
        "message": "Monthly trekking activity report generated successfully.",
        "report_file": report_file.name,
        "year": year,
        "month": month,
    }


@celery.task(name="backend.tasks.export_trekking_history")
def export_trekking_history(user_id, job_id):
    """Generate a trekker's history csv asynchronously."""
    
    export_dir = Path(current_app.root_path) / "exports"
    jobs_dir = export_dir / "jobs"
    export_dir.mkdir(parents=True, exist_ok=True)
    jobs_dir.mkdir(parents=True, exist_ok=True)

    job_file = jobs_dir / f"{job_id}.json"
    csv_file = export_dir / f"{job_id}.csv"
    
    try:
        user = db.session.get(User, user_id)
        if not user:
            return ValueError("Trekker account was not found.")

        bookings = (
            Booking.query.filter_by(usr_id=user.id)
            .filter(Booking.status.in_(["Completed", "Cancelled"]))
            .order_by(Booking.booking_date.desc(), Booking.id.desc())            
            .all()
            )

        with csv_file.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Booking ID", "Trek Name", "Location", "Booking Date", "Trek Date", "Booking Status", "Progress"
            ])

            for booking in bookings:
                schedule = db.session.get(Availability, booking.availability_id)
                trek = db.session.get(Trek, booking.trek_id)
                start = schedule.start_date if schedule else None
                end = schedule.end_date if schedule else None

                trek_date = (
                    start.strftime("%d-%m-%Y")
                    if start == end else
                    f"{start.strftime('%d-%m-%Y')} to {end.strftime('%d-%m-%Y')}"
                    if start and end else ""
                )


                writer.writerow([
                    booking.id,
                    trek.trek_name if trek else "N/A",
                    trek.location if trek else "N/A",
                    booking.booking_date.strftime("%d-%m-%Y") if booking.booking_date else "",
                    trek_date,                    
                    booking.status,
                    schedule.progress_status if schedule else "N/A",
                ])

        result = {
            "status": "completed",
            "user_id": user_id,
            "filename": csv_file.name,
            "message": "Your trekking history CSV has been exported.",
            "record_count": len(bookings),
        }

        job_file.write_text(json.dumps(result), encoding="utf-8")
        return result
    
    except Exception as exc:
        current_app.logger.exception(f"CSV export failed for trekker %s: {user_id}")

        failure = {
            "status": "failed",
            "user_id": user_id,
            "message": "CSV export failed. Please try again.",
        }
        job_file.write_text(json.dumps(failure), encoding="utf-8")
        raise

    finally:
        db.session.remove()



# end