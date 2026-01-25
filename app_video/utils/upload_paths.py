import os

from django.utils.text import slugify


def get_media_upload_path(instance: any, filename: str) -> str:
    title_slug: str = slugify(instance.title)
    _, ext = os.path.splitext(filename)
    return os.path.join(title_slug, f"{title_slug}{ext.lower()}")