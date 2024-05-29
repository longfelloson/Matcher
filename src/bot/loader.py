from aiogram import Dispatcher, Bot

from src.config import get_bot_info

bot = Bot(**get_bot_info())
dp = Dispatcher()
