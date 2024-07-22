import aiohttp
from aiogram.types import File

from bot.loader import bot
from config import settings


async def get_file_from_telegram(file_id: str) -> bytes:
    """
    Возвращает файл с серверов Телеграм в виде байтов
    """
    file: File = await bot.get_file(file_id)

    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://api.telegram.org/file/bot{settings.BOT.TOKEN}/{file.file_path}")
        return await response.read()
