# tasks.py

from datetime import date

from celery_app import celery
from database import db
from model import Availability, Trek, Booking


@celery.task(name="tasks.update_trek_progress")
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
