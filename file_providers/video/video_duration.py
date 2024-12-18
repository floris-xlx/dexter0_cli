from utils.log import log_message
import os
import subprocess


def get_video_duration(file_path):
    """Get the duration of a video file using ffmpeg."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-i", file_path],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        for line in result.stderr.splitlines():
            if "Duration" in line:
                return line.split(",")[0].split("Duration:")[1].strip()
    except Exception as e:
        log_message(os.path.basename(file_path), f"Error getting video duration: {e}")
    return None
