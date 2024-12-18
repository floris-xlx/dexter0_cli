import hashlib
import os
from tqdm import tqdm
from utils.log import log_message


def calculate_checksum(file_path, algorithm="sha256"):
    """Calculate the checksum of a file using the specified algorithm."""
    try:
        hash_func = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in tqdm(
                    iter(lambda: f.read(8192), b""),
                    desc="Calculating checksum",
                    unit="chunk",
            ):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        log_message(os.path.basename(file_path),
                    f"Error calculating checksum: {e}")
        return None