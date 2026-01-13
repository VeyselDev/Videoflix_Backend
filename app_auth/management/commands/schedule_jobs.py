from django.core.management.base import BaseCommand
from app_auth.scheduler import schedule_delete_inactive_users

class Command(BaseCommand):
    help = "Schedule recurring background jobs"

    def handle(self, *args: tuple[any, ...], **options: dict[str, any]) -> None:
        schedule_delete_inactive_users()
        self.stdout.write(self.style.SUCCESS("Jobs scheduled"))
