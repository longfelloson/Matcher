from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from bot.storage import storage
from config import settings

bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)
