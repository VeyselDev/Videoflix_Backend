from app_video.services.video_service import convert_video_to_hls


def convert_video_to_hls_job(video_id: int) -> None:
    """
    Background job that triggers HLS conversion for a video.

    This function is intended to be executed by a queue worker (e.g. RQ)
    and delegates the actual processing to the video service layer.

    Args:
        video_id: ID of the Video to convert.
    """
    convert_video_to_hls(video_id)