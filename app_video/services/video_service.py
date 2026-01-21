import logging
import os
import shutil
from pathlib import Path
from typing import List, Dict

from rest_framework.generics import get_object_or_404

from app_video.models import Video, VideoStatus
from app_video.utils.ffmpeg_utils import run_hls_conversion, HLSConfig
from app_video.utils.path_utils import (
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


class VideoService:
    def get_video_or_404(self, video_id: int) -> Video:
        return get_object_or_404(Video, id=video_id)


    def get_hls_converted_videos(self) -> List[Video]:
        return list(Video.objects.filter(status=VideoStatus.CONVERTED).order_by('-created_at'))


    def get_hls_file_path_or_404(self, video: Video, resolution: str, filename: str) -> str:
        hls_file_path: str = self.get_hls_file_path(video, resolution, filename)
        return get_file_path_or_404(hls_file_path)


    def update_video_status(self, video_id: int, status: VideoStatus) -> None:
        Video.objects.filter(pk=video_id).update(status=status)


    def convert_video_to_hls(self, video_id: int) -> None:
        video: Video = self.get_video_or_404(video_id)

        if not file_path_exists(video.file.path):
            logger.error(f'File missing: {video.file.path}')
            return

        video_dir: str = get_file_dir(video.file.path)

        for resolution_label, resolution_size in VIDEO_RESOLUTIONS.items():
            self._convert_video_to_hls_resolution(video.file.path, video_dir, resolution_label, resolution_size)

        self.update_video_status(video.pk, VideoStatus.CONVERTED)


    def delete_video_files(self, video: Video) -> None:
        video_field_names: List[str] = ['file', 'thumbnail']

        for video_field_name in video_field_names:
            media_file = getattr(video, video_field_name, None)
            if not media_file:
                continue

            file_dir: str = get_file_dir(media_file.path)
            shutil.rmtree(file_dir, ignore_errors=True)


    def _convert_video_to_hls_resolution(
        self,
        video_file_path: str,
        video_dir: str,
        resolution_label: str,
        resolution_size: str
    ) -> None:
        hls_dir: str = self.get_hls_dir(video_dir, resolution_label)
        os.makedirs(hls_dir, exist_ok=True)

        config: HLSConfig = HLSConfig(
            input_path=Path(video_file_path),
            resolution=resolution_size,
            segment_file_pattern=Path(hls_dir) / '%03d.ts',
            manifest_path=Path(hls_dir) / 'index.m3u8',
        )

        run_hls_conversion(config)
        logger.info(f'HLS {resolution_label} created for {video_file_path}')


    def get_hls_dir(self, video_dir: str, resolution: str) -> str:
        return os.path.join(video_dir, HLS_DIRECTORY_NAME, resolution)

    def get_hls_file_path(self, video: Video, resolution: str, filename: str) -> str:
        video_dir: str = get_file_dir(video.file.path)
        return os.path.join(video_dir, HLS_DIRECTORY_NAME, resolution, filename)
