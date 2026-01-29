import os
from django.utils.text import slugify

def slug_field_path(instance, filename, field_name: str) -> str:
    field_value = getattr(instance, field_name)
    slug = slugify(field_value)
    _, ext = os.path.splitext(filename)
    return os.path.join(slug, f"{slug}{ext.lower()}")


def video_file_path(instance, filename):
    return slug_field_path(instance, filename, "title")


def video_thumbnail_path(instance, filename):
    return slug_field_path(instance, filename, "title")
