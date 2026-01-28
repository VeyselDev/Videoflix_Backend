import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from core.utils.logging_utils import log_info, log_error

DEFAULT_HLS_PROFILE: List[str] = [
    '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast',
    '-c:a', 'aac', '-b:a', '128k',
    '-f', 'hls', '-hls_time', '10', '-hls_playlist_type', 'vod',
]

@dataclass
class HLSConfig:
    input_path: Path
    resolution: str
    segment_file_pattern: Path
    manifest_path: Path
    additional_options: Optional[List[str]] = field(default_factory=list)

def build_hls_command(config: HLSConfig) -> List[str]:
    return [
        'ffmpeg',
        '-hide_banner',
        '-loglevel', 'error',
        '-i', str(config.input_path),
        '-vf', f'scale={config.resolution}',
        *DEFAULT_HLS_PROFILE,
        *config.additional_options,
        '-hls_segment_filename', str(config.segment_file_pattern),
        str(config.manifest_path),
    ]

def run_hls_conversion(config: HLSConfig) -> None:
    cmd: List[str] = build_hls_command(config)

    try:
        log_info("Starting HLS conversion: %s -> %s", config.input_path, config.resolution)
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        log_info("HLS conversion completed successfully: %s", config.manifest_path)
    except subprocess.CalledProcessError as e:
        log_error(
            "FFmpeg error for %s:\nstdout:\n%s\nstderr:\n%s",
            config.input_path,
            e.stdout,
            e.stderr
        )
        raise RuntimeError(f"HLS conversion failed for {config.input_path}\nFFmpeg stderr:\n{e.stderr}") from e
