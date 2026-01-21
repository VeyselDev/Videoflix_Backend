from pathlib import Path
import json
from django.core.management.base import BaseCommand
from django.core.files import File
from app_video.models import Video


class Command(BaseCommand):
    help = "Uploads videos and thumbnails from seed_data/videos.json and media folder"

    SEED_FILE = Path("seed_data/videos.json")
    MEDIA_DIR = Path("seed_data/media")

    REQUIRED_FIELDS = ["title", "description", "category", "videoFile", "thumbnailFile"]

    def handle(self, *args, **options):
        if not self.SEED_FILE.exists():
            self.stdout.write(self.style.ERROR(f"Seed file not found: {self.SEED_FILE}"))
            return
        if not self.MEDIA_DIR.exists():
            self.stdout.write(self.style.ERROR(f"Media directory not found: {self.MEDIA_DIR}"))
            return

        with self.SEED_FILE.open("r", encoding="utf-8") as f:
            videos_data = json.load(f)

        for video_meta in videos_data:
            missing_fields = [field for field in self.REQUIRED_FIELDS if not video_meta.get(field)]
            if missing_fields:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping video, missing fields: {', '.join(missing_fields)}"
                    )
                )
                continue

            title = video_meta["title"]

            if Video.objects.filter(title=title).exists():
                self.stdout.write(self.style.WARNING(f"Video '{title}' already exists, skipping"))
                continue

            video_path = self.MEDIA_DIR / video_meta["videoFile"]
            thumbnail_path = self.MEDIA_DIR / video_meta["thumbnailFile"]

            if not video_path.exists() or not thumbnail_path.exists():
                self.stdout.write(
                    self.style.WARNING(f"Skipping '{title}', video or thumbnail file not found")
                )
                continue

            video = Video(
                title=title,
                description=video_meta["description"],
                category=video_meta["category"],
            )

            with video_path.open("rb") as v_file, thumbnail_path.open("rb") as t_file:
                video.file.save(video_path.name, File(v_file), save=False)
                video.thumbnail.save(thumbnail_path.name, File(t_file), save=False)

            video.save()
            self.stdout.write(self.style.SUCCESS(f"Uploaded video '{title}'"))
