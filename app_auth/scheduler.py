from datetime import datetime, timezone, timedelta
import django_rq
from django.conf import settings

from app_auth.tasks import delete_inactive_users


def schedule_delete_inactive_users():
    """
    Schedule a job to delete inactive users every hour.
    Ensures no duplicate jobs are scheduled.
    """
    job_path = 'app_auth.tasks.delete_inactive_users'
    interval_hours = 1

    scheduler = django_rq.get_scheduler(settings.RQ_DEFAULT_QUEUE)
    existing_jobs = {job.func for job in scheduler.get_jobs()}

    if job_path not in existing_jobs:
        scheduler.schedule(
            scheduled_time=datetime.now(timezone.utc),
            func=delete_inactive_users,
            interval=timedelta(hours=interval_hours).total_seconds(),
            repeat=-1
        )
