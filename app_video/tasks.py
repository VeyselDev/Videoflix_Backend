import logging
import subprocess
import os

from app_video.models import Video

logger = logging.getLogger(__name__)

def convert_video_to_hls(video_id):
    try:
        video = Video.objects.get(id=video_id)
        video_path = video.video_file.path

        logger.info(f'Starting HLS conversion for video ID {video_id}')
        logger.info(f'Video path: {video_path}')

    except Video.DoesNotExist:
        logger.error(f'Video with ID {video_id} not found')
        return

    if not os.path.exists(video_path):
        logger.error(f'Video file does not exist: {video_path}')
        return

    base_dir = os.path.dirname(video_path)

    resolutions = {
        '480p': '854x480',
        '720p': '1280x720',
        '1080p': '1920x1080',
    }

    for label, size in resolutions.items():
        hls_dir = os.path.join(base_dir, 'hls', label)
        os.makedirs(hls_dir, exist_ok=True)

        playlist_path = os.path.join(hls_dir, 'index.m3u8')
        segment_pattern = os.path.join(hls_dir, '%03d.ts')

        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'scale={size}',
            '-c:v', 'libx264',
            '-crf', '23',
            '-preset', 'veryfast',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-f', 'hls',
            '-hls_time', '10',
            '-hls_playlist_type', 'vod',
            '-hls_segment_filename', segment_pattern,
            playlist_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f'FFmpeg error for {label}: {result.stderr}')
        else:
            logger.info(f'Successfully created {label}')
            logger.info(f'Files: {os.listdir(hls_dir)}')
