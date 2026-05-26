import os
from django.utils.text import slugify


def slug_field_path(instance, filename, field_name: str) -> str:
    """
    Builds a filesystem upload path based on a slugified model field value.

    This ensures consistent, SEO-friendly directory and file naming.

    Args:
        instance: Model instance containing the field.
        filename: Original uploaded filename.
        field_name: Model attribute used to generate the slug.

    Returns:
        Relative upload path as a string.
    """
    field_value = getattr(instance, field_name)
    slug = slugify(field_value)
    _, ext = os.path.splitext(filename)
    return os.path.join(slug, f"{slug}{ext.lower()}")


def video_file_path(instance, filename):
    """
    Upload path generator for video files.

    Uses the video's title as the base folder and filename.
    """
    return slug_field_path(instance, filename, "title")


def video_thumbnail_path(instance, filename):
    """
    Upload path generator for video thumbnail images.

    Uses the video's title as the base folder and filename.
    """
    return slug_field_path(instance, filename, "title")