import os
import json


def get_folder_info(folder_path, show_hidden_folders=False):
    """
    Returns information about the given folder_path, including:
    - Number of files in the folder
    - List of files in a JSON array
    - Total storage used in the folder (in bytes)
    - Optionally includes hidden files and folders if show_hidden_folders is True
    """
    if not os.path.isdir(folder_path):
        return json.dumps({"error": "Invalid folder path"})

    file_list = []
    total_size = 0

    for root, dirs, files in os.walk(folder_path):
        if not show_hidden_folders:
            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            # Filter out hidden files
            files = [f for f in files if not f.startswith(".")]

        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), start=folder_path)
            file_list.append(file_path)
            total_size += os.path.getsize(os.path.join(root, file))

    folder_info = {
        "file_count": len(file_list),
        "files": file_list,
        "total_size_bytes": total_size
    }

    return json.dumps(folder_info, indent=4)
