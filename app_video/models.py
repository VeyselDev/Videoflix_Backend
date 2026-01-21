from django.db import models

from app_video.utils.path_utils import get_media_upload_path


class VideoCategory(models.TextChoices):
    ACTION = 'action', 'Action'
    COMEDY = 'comedy', 'Comedy'
    DOCUMENTARY = 'documentary', 'Documentary'
    DRAMA = 'drama', 'Drama'
    HORROR = 'horror', 'Horror'


class VideoStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    CONVERTED = 'converted', 'Converted'
    FAILED = 'failed', 'Failed'


class Video(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=32, choices=VideoCategory.choices, db_index=True)
    file = models.FileField(upload_to=get_media_upload_path)
    thumbnail = models.ImageField(upload_to=get_media_upload_path)
    status = models.CharField(max_length=16, choices=VideoStatus.choices, default=VideoStatus.PENDING, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else None

    def __str__(self):
        return self.title