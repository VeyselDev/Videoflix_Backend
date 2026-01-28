from django.core.management.base import BaseCommand
from app_auth.scheduler import register_recurring_jobs
from core.utils.logging_utils import log_info, log_exception


class Command(BaseCommand):
    help = "Schedule recurring background jobs"

    def handle(self, *args: any, **options: dict[str, any]) -> None:
        log_info("=== Starting job registration ===")
        try:
            register_recurring_jobs()
            log_info("All jobs registered successfully")
        except Exception as e:
            log_exception("Failed to register recurring jobs: %s", e)
        finally:
            log_info("=== Job registration command finished ===")
