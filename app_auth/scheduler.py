from app_auth.jobs import delete_inactive_users_job
from app_auth.services.scheduler_service import schedule_job_if_not_exists


def register_recurring_jobs() -> None:
    schedule_job_if_not_exists(delete_inactive_users_job, interval_hours=1)
