import logging

from app_video.models import VideoStatus
from app_video.services.video_service import VideoService

logger: logging.Logger = logging.getLogger(__name__)
video_service: VideoService = VideoService()


def convert_video_to_hls(video_id: int) -> None:
    logger.info("Start HLS processing for video %d", video_id)
    video_service.update_video_status(video_id, VideoStatus.PROCESSING)
    video_service.convert_video_to_hls(video_id)
