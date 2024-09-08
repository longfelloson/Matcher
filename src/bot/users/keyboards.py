from aiogram.types import KeyboardButton as Button
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from bot.users.enums import UserStatus, UserProfileSection


def user_profile_keyboard(guess_age: bool, user_status: UserStatus):
    """Клавиатура настройки пользовательского профиля"""
    # builder = Builder().row(
    #     Button(text=f"Угадывать возраст: {'✅' if guess_age else '❌'}"),
    # )
    builder = Builder().row(
        Button(text="Изменить анкету 📝")
    )

    if user_status == UserStatus.active:
        builder.row(
            Button(text="Отключить анкету 😴")
        )
    else:
        builder.row(
            Button(text="Включить анкету 🚀")
        )

    builder.row(
        Button(text="↩")
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
        Button(text="↩")
    )
    return builder.adjust(2).as_markup(resize_keyboard=True, one_time_keyboard=True)
