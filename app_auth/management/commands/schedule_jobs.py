import logging
from django.core.management.base import BaseCommand
from app_auth.scheduler import register_recurring_jobs

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Schedule recurring background jobs"

    def handle(self, *args: any, **options: dict[str, any]) -> None:
        logger.info("=== Starting job registration ===")
        try:
            register_recurring_jobs()
            logger.info("All jobs registered successfully")
        except Exception as e:
            logger.exception("Failed to register recurring jobs: %s", e)
        finally:
            logger.info("=== Job registration command finished ===")
