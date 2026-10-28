from celery import Celery
from celery.schedules import crontab
from backend.app import app


celery = Celery(
    app.import_name,
    broker=app.config["CELERY_BROKER_URL"],
    backend=app.config["CELERY_RESULT_BACKEND"],
    include=["backend.tasks"]
)

celery.conf.update(
    timezone=app.config.get("CELERY_TIMEZONE", "Asia/Kolkata"),
    enable_utc=app.config.get("CELERY_ENABLE_UTC", True),

    beat_schedule={
        # Existing task: update trek progress every day at 12:05 AM.
        "update-trek-progress-daily": {
            "task": "backend.tasks.update_trek_progress",
            "schedule": crontab(hour=0, minute=5),
        },
        # New task: send trek reminders every day at 8:00 AM.
        "daily-trek-reminders": {
            "task": "backend.tasks.send_trek_reminders",
            "schedule": crontab(hour=8, minute=0),
        },
        # New task: generate a report on the first day of each month.
        "monthly-trekking-report": {
            "task": "backend.tasks.generate_monthly_report",
            "schedule": crontab(day_of_month=1, hour=1, minute=0),
        },
    }
)


class FlaskContextTask(celery.Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = FlaskContextTask