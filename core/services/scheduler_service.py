from datetime import datetime, timezone, timedelta
import django_rq
from django.conf import settings
from typing import Callable

from rq_scheduler import Scheduler


def get_scheduler(queue_name: str = settings.DEFAULT_QUEUE) -> Scheduler:
    """
    Returns an RQ Scheduler instance for the given queue.

    Args:
        queue_name: Name of the RQ queue.

    Returns:
        Scheduler instance bound to that queue.
    """
    return django_rq.get_scheduler(queue_name)


def job_exists(scheduler, job_func: Callable) -> bool:
    """
    Checks whether a given job function is already scheduled.

    Compares the fully qualified function path against existing scheduled jobs.

    Args:
        scheduler: RQ Scheduler instance.
        job_func: Function to check.

    Returns:
        True if job is already scheduled, otherwise False.
    """
    job_path = f"{job_func.__module__}.{job_func.__name__}"
    existing_jobs = {job.func for job in scheduler.get_jobs()}
    return job_path in existing_jobs


def schedule_job_if_not_exists(
    job_func: Callable,
    interval_hours: int,
    queue_name: str = settings.DEFAULT_QUEUE
) -> None:
    """
    Schedules a recurring job if it is not already registered.

    The job will:
    - Start immediately
    - Repeat at a fixed interval
    - Run indefinitely until explicitly removed

    Args:
        job_func: Function to schedule.
        interval_hours: Execution interval in hours.
        queue_name: Target RQ queue name.
    """
    scheduler = get_scheduler(queue_name)

    if not job_exists(scheduler, job_func):
        scheduler.schedule(
            scheduled_time=datetime.now(timezone.utc),
            func=job_func,
            interval=timedelta(hours=interval_hours).total_seconds(),
            repeat=-1
        )