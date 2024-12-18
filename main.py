import argparse
import os
import asyncio
from colorama import Fore, Style

from webdav_client.client import initialize_webdav_client, upload_file, upload_folder


async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="CLI tool to upload files or folders to WebDAV.")
    parser.add_argument("--file", type=str, help="Path to the file to upload.")
    parser.add_argument("--folder",
                        type=str,
                        help="Path to the folder to upload.")
    parser.add_argument(
        "--webdav_path",
        type=str,
        required=True,
        help="Remote WebDAV path where the file or folder will be uploaded.")
    args = parser.parse_args()

    # Validate WebDAV path
    if not args.webdav_path.startswith("/"):
        print(Fore.RED + "Error: The WebDAV path must start with '/'." +
              Style.RESET_ALL)
        return

    # Initialize WebDAV client
    try:
        client = initialize_webdav_client()
        if client is None:
            raise ValueError(
                "WebDAV client initialization returned None. Check your environment variables."
            )
    except (AttributeError, ValueError) as e:
        print(Fore.RED + f"Error initializing WebDAV client: {e}" +
              Style.RESET_ALL)
        return

    # Handle file or folder upload
    if args.file:
        file_path = args.file
        print(Fore.CYAN + f"Preparing to upload file: {file_path}" + Style.RESET_ALL)
        if not os.path.isfile(file_path):
            print(Fore.RED + f"Error: File {file_path} does not exist." +
                  Style.RESET_ALL)
            return
        print(Fore.BLUE +
              f"Uploading file {file_path} to {args.webdav_path}..." +
              Style.RESET_ALL)
        try:
            success = upload_file(client, file_path, args.webdav_path)
            if success:
                print(
                    Fore.GREEN +
                    f"File {file_path} uploaded successfully to {args.webdav_path}."
                    + Style.RESET_ALL)
            else:
                print(
                    Fore.RED +
                    f"Failed to upload file {file_path} to {args.webdav_path}."
                    + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error during file upload: {e}" +
                  Style.RESET_ALL)

    elif args.folder:
        folder_path = args.folder
        print(Fore.CYAN + f"Preparing to upload folder: {folder_path}" + Style.RESET_ALL)
        if not os.path.isdir(folder_path):
            print(Fore.RED + f"Error: Folder {folder_path} does not exist." +
                  Style.RESET_ALL)
            return
        print(Fore.BLUE +
              f"Uploading folder {folder_path} to {args.webdav_path}..." +
              Style.RESET_ALL)
        try:
            upload_folder(client, folder_path, args.webdav_path)
            print(
                Fore.GREEN +
                f"Folder {folder_path} uploaded successfully to {args.webdav_path}."
                + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error during folder upload: {e}" +
                  Style.RESET_ALL)
    else:
        print(Fore.RED + "Error: You must specify either --file or --folder." +
              Style.RESET_ALL)


if __name__ == "__main__":
    asyncio.run(main())
