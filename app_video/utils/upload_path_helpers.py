import os

from django.utils.text import slugify


def build_upload_path(instance, filename):
    title_slug = slugify(instance.title)
    _, ext = os.path.splitext(filename)
    return os.path.join(title_slug, f"{title_slug}{ext.lower()}")

def video_upload_path(instance, filename):
    return build_upload_path(instance, filename)

def thumbnail_upload_path(instance, filename):
    return build_upload_path(instance, filename)