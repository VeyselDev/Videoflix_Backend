import json
from pathlib import Path
from typing import TypedDict, List, Tuple, NamedTuple

from django.conf import settings
from django.core.files import File
from django.db import transaction

from app_video.models.video import Video
from core.utils.logging_utils import log_warning, log_info, log_error

TEXT_ENCODING = "utf-8"
BINARY_MODE = "rb"

SEED_DIR = settings.BASE_DIR / "seed_data"
VIDEO_META_FILE = SEED_DIR / "videos.json"


class MediaDirs(NamedTuple):
    video: Path
    thumbnail: Path


MEDIA_DIRS = MediaDirs(
    video=SEED_DIR / "videos",
    thumbnail=SEED_DIR / "thumbnails",
)


class VideoMetadata(TypedDict):
    title: str
    description: str
    category: str
    videoFile: str
    thumbnailFile: str


REQUIRED_FIELDS = list(VideoMetadata.__annotations__.keys())


def seed_videos() -> None:
    if not _are_seed_resources_available():
        return

    for meta in _load_video_metadata():
        _seed_video(meta)


def _are_seed_resources_available() -> bool:
    required_paths = [
        VIDEO_META_FILE,
        MEDIA_DIRS.video,
        MEDIA_DIRS.thumbnail,
    ]

    for path in required_paths:
        if not path.exists():
            log_error(f"Resource missing: {path}")
            return False
    return True


def _load_video_metadata() -> List[VideoMetadata]:
    with VIDEO_META_FILE.open(encoding=TEXT_ENCODING) as file:
        return json.load(file)


def _seed_video(meta: VideoMetadata) -> None:
    if not _is_valid_metadata(meta):
        return

    title = meta["title"]

    if Video.objects.filter(title=title).exists():
        log_warning(f"Skipping: Video '{title}' already exists.")
        return

    try:
        video_path, thumb_path = _resolve_media_paths(meta)

        if not _files_exist(video_path, thumb_path):
            return

        _create_video(meta, video_path, thumb_path)
        log_info(f"Successfully seeded: {title}")

    except FileNotFoundError as exc:
        log_error(f"File error for '{title}': {exc}")


def _is_valid_metadata(meta: VideoMetadata) -> bool:
    missing = [field for field in REQUIRED_FIELDS if not meta.get(field)]
    if missing:
        log_warning(f"Invalid metadata. Missing: {', '.join(missing)}")
        return False
    return True


def _resolve_media_paths(meta: VideoMetadata) -> Tuple[Path, Path]:
    return (
        MEDIA_DIRS.video / meta["videoFile"],
        MEDIA_DIRS.thumbnail / meta["thumbnailFile"],
    )


def _files_exist(*paths: Path) -> bool:
    for path in paths:
        if not path.exists():
            log_warning(f"Media file not found: {path}")
            return False
    return True


@transaction.atomic
def _create_video(meta: VideoMetadata, video_path: Path, thumb_path: Path) -> None:
    video = Video(
        title=meta["title"],
        description=meta["description"],
        category=meta["category"],
    )

    with video_path.open(BINARY_MODE) as v_file, thumb_path.open(BINARY_MODE) as t_file:
        video.file.save(video_path.name, File(v_file), save=False)
        video.thumbnail.save(thumb_path.name, File(t_file), save=False)
        video.save()