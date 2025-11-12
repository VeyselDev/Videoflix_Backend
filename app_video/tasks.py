import subprocess
import os


def convert_video_to_hls(video_path):
    base, ext = os.path.splitext(video_path)
    resolutions = {
        "480p": "854x480",
        "720p": "1280x720",
        "1080p": "1920x1080",
    }

    for label, size in resolutions.items():
        output_dir = f"{base}_{label}"
        os.makedirs(output_dir, exist_ok=True)

        playlist_path = os.path.join(output_dir, "index.m3u8")

        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"scale={size}",
            "-c:v", "libx264",
            "-crf", "23",
            "-preset", "veryfast",
            "-c:a", "aac",
            "-b:a", "128k",
            "-f", "hls",
            "-hls_time", "10",
            "-hls_playlist_type", "vod",
            "-hls_segment_filename", os.path.join(output_dir, "%03d.ts"),
            playlist_path
        ]

        subprocess.run(cmd, capture_output=True, text=True)