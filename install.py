import subprocess
import sys
import requests
import os
import yaml


def download_ffmpeg_tools():
    """Download ffmpeg tools from the URLs specified in install_paths.yaml."""
    try:
        with open("install_paths.yaml", "r") as file:
            paths = yaml.safe_load(file)  # Using pyYAML to load the YAML file

        for tool, url in paths.items():
            file_name = os.path.basename(url)  # Extract file name from URL
            print(f"Downloading {file_name} from {url}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"{file_name} downloaded successfully.")
    except yaml.YAMLError as yaml_error:
        print(f"\033[91mError parsing YAML file: {yaml_error}\033[0m")
        sys.exit(1)
    except requests.RequestException as request_error:
        print(f"\033[91mError downloading ffmpeg tools: {request_error}\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\033[91mUnexpected error: {e}\033[0m")
        sys.exit(1)


def check_ffmpeg_installed():
    """Check if ffmpeg is installed and accessible from PATH."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            print("ffmpeg is installed and accessible.")
        else:
            raise FileNotFoundError("ffmpeg is not accessible.")
    except FileNotFoundError:
        print("\033[91mError: ffmpeg is not installed or not set on PATH.\033[0m")
        print("Attempting to download ffmpeg tools...")
        download_ffmpeg_tools()
        print("Please ensure the tools are added to PATH or used directly.")
        sys.exit(1)
