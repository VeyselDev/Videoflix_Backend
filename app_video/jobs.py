from app_video.services.video_service import convert_video_to_hls


def convert_video_to_hls_job(video_id: int) -> None:
    convert_video_to_hls(video_id)
