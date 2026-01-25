from datetime import datetime, timezone, timedelta
import django_rq
from django.conf import settings
from typing import Callable

from rq_scheduler import Scheduler


def get_scheduler(queue_name: str = settings.DEFAULT_QUEUE) -> Scheduler:
    return django_rq.get_scheduler(queue_name)


def job_exists(scheduler, job_func: Callable) -> bool:
    job_path = f"{job_func.__module__}.{job_func.__name__}"
    existing_jobs = {job.func for job in scheduler.get_jobs()}
    return job_path in existing_jobs


def schedule_job_if_not_exists(job_func: Callable, interval_hours: int, queue_name: str = settings.DEFAULT_QUEUE) -> None:
    scheduler = get_scheduler(queue_name)

    if not job_exists(scheduler, job_func):
        scheduler.schedule(
            scheduled_time=datetime.now(timezone.utc),
            func=job_func,
            interval=timedelta(hours=interval_hours).total_seconds(),
            repeat=-1
        )
