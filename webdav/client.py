from webdav3.client import Client
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from a .env file
load_dotenv()


async def initialize_webdav_client():
    """Asynchronously initialize and return a WebDAV client."""
    options = {
        "webdav_hostname": os.getenv("WEBDAV_HOSTNAME"),
        "webdav_login": os.getenv("WEBDAV_LOGIN"),
        "webdav_password": os.getenv("WEBDAV_PASSWORD"),
    }
    client = Client(options)
    client.verify = True
    await asyncio.sleep(0)  # Simulate async behavior if needed
    return client
