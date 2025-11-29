import os
from datetime import datetime

from django.db import models
from django.utils.text import slugify


def build_upload_path(self, filename, folder):
    title_slug = slugify(self.title)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(filename)
    new_filename = f"{timestamp}_{slugify(base)}{ext}"
    return os.path.join(folder, title_slug, new_filename)

def video_upload_path(self, filename):
    return build_upload_path(self, filename, "videos")

def thumbnail_upload_path(self, filename):
    return build_upload_path(self, filename, "thumbnails")


class Video(models.Model):
    CATEGORY_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('documentary', 'Documentary'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, db_index=True)
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