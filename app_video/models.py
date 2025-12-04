import os

from django.db import models
from django.utils.text import slugify


def build_upload_path(instance, filename, prefix):
    title_slug = slugify(instance.title)
    _, ext = os.path.splitext(filename)
    return os.path.join(title_slug, f"{prefix}{ext.lower()}")

def video_upload_path(instance, filename):
    return build_upload_path(instance, filename, "video")

def thumbnail_upload_path(instance, filename):
    return build_upload_path(instance, filename, "thumbnail")


class Video(models.Model):
    CATEGORY_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('documentary', 'Documentary'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
    ]
    title = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, blank=False, null=False, db_index=True)
    video_file = models.FileField(upload_to=video_upload_path, blank=False, null=False)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_path, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return None

    def __str__(self):
        return self.title