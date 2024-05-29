from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup as InlineKeyboard, InlineKeyboardButton as InlineButton
from aiogram.utils.keyboard import InlineKeyboardBuilder as InlineBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from src.users.configs.models import UserConfig


def user_profile_keyboard(config: UserConfig):
    """
    Клавиатура настройки пользовательского профиля
    """
    builder = Builder().row(
        Button(text=f"Угадывать возраст: {'✅' if config.guess_age else '❌'}"),
    )
    builder.row(
        Button(text="Изменить 📝")
    )
    builder.row(
        Button(text="↩")
    )
    return builder.as_markup(resize_keyboard=True)


def change_user_profile_section_keyboard():
    """
    Клавиатура смены данных профиля пользователя
    """
    profile_sections = ["Имя", "Возраст", "Город"]
    builder = Builder()

    for profile_section in profile_sections:
        builder.row(Button(text=profile_section))

    builder.row(Button(text="↩"))
    return builder.as_markup(resize_keyboard=True)
