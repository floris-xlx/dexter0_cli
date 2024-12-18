import hashlib
from utils.log import log_message

def calculate_upload_hash(file_type, size_in_bytes, checksum):
    """Generate an MD5 hash based on file_type, size_in_bytes, and checksum."""
    try:
        hash_input = f"{file_type}|{size_in_bytes}|{checksum}".encode("utf-8")
        return hashlib.md5(hash_input).hexdigest()
    except Exception as e:
        log_message("general", f"Error calculating upload hash: {e}")
        return None