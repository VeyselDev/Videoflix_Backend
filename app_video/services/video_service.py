import logging
import os
import shutil
from pathlib import Path
from typing import List, Dict

from django.utils.text import slugify
from rest_framework.generics import get_object_or_404

from app_video.models import Video, VideoStatus
from app_video.utils.ffmpeg_utils import run_hls_conversion, HLSConfig
from core.utils.path_utils import (
    get_file_path_or_404,
    file_path_exists,
    get_file_dir,
)


logger = logging.getLogger(__name__)

VIDEO_RESOLUTIONS: Dict[str, str] = {
    '480p': '854x480',
    '720p': '1280x720',
    '1080p': '1920x1080',
}

HLS_DIRECTORY_NAME: str = 'hls'


def get_video_or_404(video_id: int) -> Video:
    return get_object_or_404(Video, id=video_id)


def get_hls_converted_videos() -> List[Video]:
    return list(Video.objects.filter(status=VideoStatus.CONVERTED).order_by('-created_at'))


def get_hls_file_path_or_404(video: Video, resolution: str, filename: str) -> str:
    hls_file_path: str = get_hls_file_path(video, resolution, filename)
    return get_file_path_or_404(hls_file_path)


def update_video_status(video_id: int, status: VideoStatus) -> None:
    Video.objects.filter(pk=video_id).update(status=status)


def convert_video_to_hls(video_id: int) -> None:
    video: Video = get_video_or_404(video_id)
    update_video_status(video.pk, VideoStatus.PROCESSING)

    if not file_path_exists(video.file.path):
        logger.error("File missing: %s", video.file.path)
        update_video_status(video.pk, VideoStatus.FAILED)
        raise FileNotFoundError(f"File missing: {video.file.path}")

    try:
        video_dir: str = get_file_dir(video.file.path)
        for label, size in VIDEO_RESOLUTIONS.items():
            _convert_video_to_hls_resolution(
                video.file.path,
                video_dir,
                label,
                size,
            )
    except Exception as e:
        logger.exception("Error converting video %s", video.pk)
        update_video_status(video.pk, VideoStatus.FAILED)
        raise e

    update_video_status(video.pk, VideoStatus.CONVERTED)


def delete_video_files(video: Video) -> None:
    video_field_names: List[str] = ['file', 'thumbnail']

    for video_field_name in video_field_names:
        media_file = getattr(video, video_field_name, None)
        if not media_file:
            continue

        file_dir: str = get_file_dir(media_file.path)
        shutil.rmtree(file_dir, ignore_errors=True)


def _convert_video_to_hls_resolution(
    video_file_path: str,
    video_dir: str,
    resolution_label: str,
    resolution_size: str
) -> None:
    hls_dir: str = get_hls_dir(video_dir, resolution_label)
    os.makedirs(hls_dir, exist_ok=True)

    config: HLSConfig = HLSConfig(
        input_path=Path(video_file_path),
        resolution=resolution_size,
        segment_file_pattern=Path(hls_dir) / '%03d.ts',
        manifest_path=Path(hls_dir) / 'index.m3u8',
    )

    try:
        run_hls_conversion(config)
        logger.info(f'HLS {resolution_label} created for {video_file_path}')
    except Exception as e:
        logger.error(f'Failed HLS {resolution_label} for {video_file_path}: {e}')
        raise


def get_hls_dir(video_dir: str, resolution: str) -> str:
    return os.path.join(video_dir, HLS_DIRECTORY_NAME, resolution)


def get_hls_file_path(video: Video, resolution: str, filename: str) -> str:
    video_dir: str = get_file_dir(video.file.path)
    return os.path.join(video_dir, HLS_DIRECTORY_NAME, resolution, filename)


def get_media_upload_path(instance: any, filename: str) -> str:
    title_slug: str = slugify(instance.title)
    _, ext = os.path.splitext(filename)
    return os.path.join(title_slug, f"{title_slug}{ext.lower()}")
