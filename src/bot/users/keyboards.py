from aiogram.types import KeyboardButton as Button
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from bot.users.models import UserConfig


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
    profile_sections = ["Имя", "Возраст", "Город", "Фото"]
    builder = Builder()

    for profile_section in profile_sections:
        builder.add(Button(text=profile_section))

    builder.row(Button(text="↩"))
    return builder.adjust(2).as_markup(resize_keyboard=True)
