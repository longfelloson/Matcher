from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from config import settings

bot = Bot(token=settings.BOT.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
