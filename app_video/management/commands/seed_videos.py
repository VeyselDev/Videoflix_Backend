from django.core.management.base import BaseCommand

from app_video.services.seed_video_service import seed_videos


class Command(BaseCommand):
    """
    Django management command to seed initial video data.

    Loads and processes video entries from a predefined JSON seed file.
    """
    help = "Uploads videos from seed_data/videos.json"

    def handle(self, *args, **options) -> None:
        """
        Executes the seeding process.

        This command is typically used for initial setup or local development
        to populate the database with sample video entries.
        """
        seed_videos()