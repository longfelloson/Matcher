import aiohttp
from aiogram.types import File

from bot.loader import bot
from config import settings
from s3 import s3_client

BASE_TELEGRAM_FILE_URL = "https://api.telegram.org/file/bot"
DEFAULT_FILE_EXTENSION = "jpg"


async def get_file_from_telegram(file_id: str) -> bytes:
    """Returns file by given ID from Telegram's server"""
    file: File = await bot.get_file(file_id)

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"{BASE_TELEGRAM_FILE_URL}{settings.BOT_TOKEN}/{file.file_path}"
        )
        return await response.read()


async def upload_user_photo_to_s3(
    telegram_file_id: str, extension: str = DEFAULT_FILE_EXTENSION
) -> None:
    file = await get_file_from_telegram(telegram_file_id)
    filename = f"{telegram_file_id}.{extension}"

    await s3_client.upload_file(filename, file)
