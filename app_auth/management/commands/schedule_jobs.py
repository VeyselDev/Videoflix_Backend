from django.core.management.base import BaseCommand
from app_auth.scheduler import register_recurring_jobs
from core.utils.logging_utils import log_info, log_exception


class Command(BaseCommand):
    """
    Django management command to initialize and register recurring background jobs.

    This command serves as the entry point for the application's scheduling system,
    ensuring all periodic tasks (e.g., via APScheduler) are properly enqueued.
    """

    help = "Schedule recurring background jobs"

    def handle(self, *args: any, **options: dict[str, any]) -> None:
        """
        Executes the job registration logic.

        This method wraps the registration process in a try-except block to ensure
        system stability and provides comprehensive logging for monitoring purposes.

        Args:
            *args (any): Variable length argument list.
            **options (dict): Arbitrary keyword arguments (e.g., verbosity, settings).

        Returns:
            None

        Raises:
            Exception: Logs any error occurring during the job registration process
                to the exception logger but allows the command to exit gracefully.
        """
        log_info("=== Starting job registration ===")
        try:
            register_recurring_jobs()
            log_info("All jobs registered successfully")
        except Exception as e:
            # Captures and logs the stack trace and error message
            log_exception("Failed to register recurring jobs: %s", e)
        finally:
            log_info("=== Job registration command finished ===")