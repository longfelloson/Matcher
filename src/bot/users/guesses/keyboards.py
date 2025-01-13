from typing import List

from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from bot.keyboards import back_button


def guess_age_buttons_keyboard(age_range: List[int]) -> Keyboard:
    buttons = [Button(text=str(age)) for age in age_range]
    return Builder().add(*buttons).row(back_button()).as_markup(resize_keyboard=True)
