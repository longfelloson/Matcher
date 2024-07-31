import aiohttp
from aiogram.types import File

from bot.loader import bot
from config import settings
from s3 import s3_client


async def get_file_from_telegram(file_id: str) -> bytes:
    """
    Возвращает файл с серверов Телеграм в виде байтов
    """
    file: File = await bot.get_file(file_id)

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"https://api.telegram.org/file/bot{settings.BOT.BOT_TOKEN}/{file.file_path}"
        )
        return await response.read()


async def upload_user_photo_to_s3(telegram_file_id: str) -> str:
    """
    Загружает фото полученное от пользователя в хранилище S3
    """
    file = await get_file_from_telegram(telegram_file_id)
    filename = telegram_file_id + ".jpg"

    await s3_client.upload_file(filename, file)
