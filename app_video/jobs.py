import logging

from app_video.models import VideoStatus
from app_video.services.video_service import update_video_status, convert_video_to_hls

logger: logging.Logger = logging.getLogger(__name__)


def convert_video_to_hls_job(video_id: int) -> None:
    logger.info("Start HLS processing for video %d", video_id)
    update_video_status(video_id, VideoStatus.PROCESSING)
    convert_video_to_hls(video_id)
