from django.db import models

from app_video.models.video_category import VideoCategory
from app_video.models.video_status import VideoStatus
from app_video.utils.upload_path_utils import video_file_path, video_thumbnail_path


class Video(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=32, choices=VideoCategory.choices, db_index=True)
    file = models.FileField(upload_to=video_file_path)
    thumbnail = models.ImageField(upload_to=video_thumbnail_path)
    status = models.CharField(max_length=16, choices=VideoStatus.choices, default=VideoStatus.PENDING, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else None

    def __str__(self):
        return self.title