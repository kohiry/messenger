import logging

import aiofiles
from aiofiles import os
from fastapi import UploadFile


async def save_media(audio: UploadFile, path: str):
    async with aiofiles.open(path, 'wb') as f:
        while content := await audio.read(1024):
            await f.write(content)


async def create_folder(folder: str):
    await os.makedirs(folder, exist_ok=True)


def get_logger():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    return logging.getLogger(__name__)
