import os
from pathlib import Path
from typing import Optional

from django.core.files import File
from django.http import Http404
from django.utils.text import slugify


def get_media_upload_path(instance: any, filename: str) -> str:
    title_slug: str = slugify(instance.title)
    _, ext = os.path.splitext(filename)
    return os.path.join(title_slug, f"{title_slug}{ext.lower()}")


def get_file_url(file_field: File) -> Optional[str]:
    return file_field.url if file_field else None


def get_file_dir(file_path: str) -> str:
    return str(Path(file_path).parent)


def file_path_exists(file_path: str) -> bool:
    return os.path.exists(file_path)


def get_file_path_or_404(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise Http404(f"File not found: {file_path}")
    return file_path
