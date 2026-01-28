from app_video.services.video_service import convert_video_to_hls
from core.utils.logging_utils import log_info


def convert_video_to_hls_job(video_id: int) -> None:
    log_info("Start HLS processing for video %d", video_id)
    convert_video_to_hls(video_id)
