from webdav3.client import Client
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from a .env file
load_dotenv()


def initialize_webdav_client():
    """Asynchronously initialize and return a WebDAV client."""
    load_dotenv()

    options = {
       
    }

    # Validate that required options are not None
    for key, value in options.items():
        if value is None:
            raise ValueError(f"Environment variable for {key} is not set or invalid.")

    client = Client(options)
    client.verify = True

    return client


def upload_file(client, local_path, remote_path):
    """
    Upload a single file to the specified WebDAV location.

    Args:
        client (Client): The WebDAV client instance.
        local_path (str): The local file path to upload.
        remote_path (str): The remote WebDAV path where the file will be uploaded.

    Returns:
        bool: True if the upload was successful, False otherwise.
    """
    try:
        file_name = os.path.basename(local_path)
        remote_path = os.path.join(remote_path, file_name).replace("\\", "/")

        file_size = os.path.getsize(local_path)
        uploaded_size = 0

        def progress_callback(current, total):
            nonlocal uploaded_size
            increment = current - uploaded_size
            uploaded_size = current
            print(f"Uploaded {increment} bytes to {remote_path}")

        client.upload_sync(
            remote_path=remote_path,
            local_path=local_path,
            progress=progress_callback,
        )
        print(f"File uploaded successfully to {remote_path}")
        return True
    except Exception as e:
        error_message = (
            f"Error uploading file {local_path} to {remote_path}: {e}\n"
            f"Request to {client.webdav.hostname}{remote_path} failed. "
            f"Please check the file path and WebDAV server configuration."
        )
        print(error_message)
        return False


def upload_folder(client, folder_path, remote_base_path, include_hidden=False):
    """
    Recursively upload all files in a folder to the specified WebDAV location.

    Args:
        client (Client): The WebDAV client instance.
        folder_path (str): The local folder path to upload.
        remote_base_path (str): The base remote WebDAV path where files will be uploaded.
        include_hidden (bool): Whether to include hidden files and folders.

    Returns:
        None
    """
    if not os.path.isdir(folder_path):
        print(f"Invalid folder path: {folder_path}")
        return

    for root, dirs, files in os.walk(folder_path):
        if not include_hidden:
            # Exclude hidden directories and files
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            files = [f for f in files if not f.startswith(".")]

        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, start=folder_path)
            remote_file_path = os.path.join(remote_base_path,
                                            relative_path).replace("\\", "/")

            print(f"Uploading {local_file_path} to {remote_file_path}...")
            success = upload_file(client, local_file_path, remote_file_path)
            if not success:
                print(f"Failed to upload {local_file_path}")
