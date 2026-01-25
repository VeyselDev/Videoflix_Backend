import logging

from app_video.services.video_service import convert_video_to_hls

logger: logging.Logger = logging.getLogger(__name__)


def convert_video_to_hls_job(video_id: int) -> None:
    logger.info("Start HLS processing for video %d", video_id)
    convert_video_to_hls(video_id)
