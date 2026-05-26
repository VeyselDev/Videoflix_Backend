import os
from pathlib import Path
from typing import Optional

from django.core.files import File
from django.http import Http404


"""
File utility helpers for safe path handling and Django file fields.
"""


def get_file_url(file_field: File) -> Optional[str]:
    """
    Returns the URL of a Django FileField if available.

    Args:
        file_field: Django File instance or FileField value.

    Returns:
        File URL or None if not available.
    """
    return file_field.url if file_field else None


def get_file_dir(file_path: str) -> str:
    """
    Returns the directory part of a file path.

    Args:
        file_path: Absolute or relative file path.

    Returns:
        Directory path as string.
    """
    return str(Path(file_path).parent)


def file_path_exists(file_path: str) -> bool:
    """
    Checks whether a file exists on disk.

    Args:
        file_path: Path to file.

    Returns:
        True if file exists, otherwise False.
    """
    return os.path.exists(file_path)


def get_file_path_or_404(file_path: str) -> str:
    """
    Returns file path if it exists, otherwise raises Http404.

    Args:
        file_path: Path to file.

    Returns:
        Same file path if valid.

    Raises:
        Http404: If file does not exist.
    """
    if not os.path.exists(file_path):
        raise Http404(f"File not found: {file_path}")
    return file_path