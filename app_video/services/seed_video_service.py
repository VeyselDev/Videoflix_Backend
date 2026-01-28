import json
from pathlib import Path
from typing import Iterable

from django.conf import settings
from django.core.files import File

from app_video.models import Video
from core.utils.logging_utils import log_warn, log_info, log_error


SEED_FILE = settings.BASE_DIR / "seed_data/videos.json"
VIDEO_FILE_DIR = settings.BASE_DIR / "seed_data/videos"
THUMBNAIL_FILE_DIR = settings.BASE_DIR / "seed_data/thumbnails"

REQUIRED_FIELDS = (
    "title",
    "description",
    "category",
    "videoFile",
    "thumbnailFile",
)

def seed_videos() -> None:
    if not _validate_seed_sources():
        return

    for video_meta in _load_seed_data():
        _process_video(video_meta)

def _process_video(meta: dict) -> None:
    if missing := _missing_fields(meta):
        log_warn(f"Skipping video, missing fields: {', '.join(missing)}")
        return

    title = meta["title"]

    if _video_exists(title):
        log_warn(f"Video '{title}' already exists, skipping")
        return

    video_path, thumbnail_path = _resolve_media_paths(meta)

    if not _media_files_exist(video_path, thumbnail_path):
        log_warn(f"Skipping '{title}', video or thumbnail file not found")
        return

    _create_video(meta, video_path, thumbnail_path)
    log_info(f"Uploaded video '{title}'")


def _load_seed_data() -> Iterable[dict]:
    with SEED_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def _validate_seed_sources() -> bool:
    if not SEED_FILE.exists():
        log_error(f"Seed file not found: {SEED_FILE}")
        return False

    if not VIDEO_FILE_DIR.exists():
        log_error(f"Video file directory not found: {VIDEO_FILE_DIR}")
        return False

    if not THUMBNAIL_FILE_DIR.exists():
        log_error(f"Thumbnail file directory not found: {THUMBNAIL_FILE_DIR}")
        return False

    return True


def _missing_fields(meta: dict) -> list[str]:
    return [field for field in REQUIRED_FIELDS if not meta.get(field)]


def _video_exists(title: str) -> bool:
    return Video.objects.filter(title=title).exists()


def _media_files_exist(*paths: Path) -> bool:
    return all(path.exists() for path in paths)


def _resolve_media_paths(meta: dict) -> tuple[Path, Path]:
    return (
        VIDEO_FILE_DIR / meta["videoFile"],
        THUMBNAIL_FILE_DIR / meta["thumbnailFile"],
    )


def _create_video(meta: dict, video_path: Path, thumbnail_path: Path) -> None:
    video = Video(
        title=meta["title"],
        description=meta["description"],
        category=meta["category"],
    )

    with video_path.open("rb") as v_file, thumbnail_path.open("rb") as t_file:
        video.file.save(video_path.name, File(v_file), save=False)
        video.thumbnail.save(thumbnail_path.name, File(t_file), save=False)

    video.save()