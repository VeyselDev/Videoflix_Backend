from app_auth.jobs import delete_inactive_users_job
from core.services.scheduler_service import schedule_job_if_not_exists


def register_recurring_jobs() -> None:
    """
    Registers recurring background jobs with the scheduler.

    Ensures that each job is only scheduled once to prevent duplicates.

    Current jobs:
    - delete_inactive_users_job: Runs every hour to remove inactive users older than 24 hours.
    """
    schedule_job_if_not_exists(delete_inactive_users_job, interval_hours=1)