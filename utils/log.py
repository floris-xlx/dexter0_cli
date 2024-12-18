import os
import time


def log_message(file_name, message):
    """Log a message to a single log file for all processed files."""
    log_file_path = "./UPLOAD_DATA/logs/combined.log"
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    print(f"\033[1;34m{message}\033[0m")
    with open(log_file_path, "a") as log_file:
        log_file.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {file_name}: {message}\n")
