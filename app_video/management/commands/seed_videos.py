from django.core.management.base import BaseCommand

from app_video.services.seed_video_service import seed_videos


class Command(BaseCommand):
    help = "Uploads videos from seed_data/videos.json"

    def handle(self, *args, **options) -> None:
        seed_videos()