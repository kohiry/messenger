from fastapi import UploadFile


async def save_audio(audio: UploadFile):
    async with open(f'../../static/media_data_id}')