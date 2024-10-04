from typing import List

from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

USER_RATE_BUTTONS = ["❤", "👎"]


def guess_user_age_keyboard(age_range: List[int]) -> Keyboard:
    """Клавиатура с кнопками выбора возраста поиска анкет"""
    buttons = [
        Button(text=str(age)) for age in age_range
    ]
    return Builder().add(*buttons).row(Button(text="↩")).as_markup(resize_keyboard=True)


def rate_user_keyboard() -> Keyboard:
    """Кнопки оценки пользователя"""
    rate_user_buttons = [
        Button(text=text) for text in USER_RATE_BUTTONS
    ]
    builder = Builder().row(
        *rate_user_buttons
    )
    return builder.row(Button(text="↩")).as_markup(resize_keyboard=True)
