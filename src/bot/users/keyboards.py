from aiogram.types import KeyboardButton as Button
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from bot.keyboards import back_button
from bot.users.enums.sections import UserProfileSection
from bot.users.enums.statuses import UserStatus


def user_profile_keyboard(guess_age: bool, user_status: UserStatus):
    """Клавиатура настройки пользовательского профиля"""
    # builder = Builder().row(
    #     Button(text=f"Угадывать возраст: {'✅' if guess_age else '❌'}"),
    # )
    builder = Builder().row(
        Button(text="Изменить анкету 📝")
    )
    builder.row(
        Button(text="Отключить анкету 😴" if user_status == UserStatus.active else "Включить анкету 🚀")
    )
    builder.row(
        back_button()
    )
    return builder.as_markup(resize_keyboard=True)


def change_user_profile_section_keyboard():
    """Клавиатура выбора секции профиля для изменения"""
    buttons = [
        Button(text=profile_section) for profile_section in UserProfileSection
    ]
    builder = Builder().add(
        *buttons
    )
    builder.row(
        back_button()
    )
    return builder.adjust(2).as_markup(resize_keyboard=True, one_time_keyboard=True)
