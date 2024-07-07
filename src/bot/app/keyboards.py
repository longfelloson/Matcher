from aiogram.types import InlineKeyboardMarkup as InlineKeyboard, InlineKeyboardButton as InlineButton
from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.utils.keyboard import InlineKeyboardBuilder as InlineBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from bot.users.schemas import AdminActions
from config import settings


def main_keyboard() -> Keyboard:
    """
    Keyboard with main buttons
    """
    builder = Builder().row(
        Button(text="Начать ▶️")
    )
    builder.row(
        Button(text="Профиль 📱")
    )
    return builder.as_markup(resize_keyboard=True)


def help_command_keyboard() -> InlineKeyboard:
    """
    Help's command keyboard
    """
    keyboard = [[
        InlineButton(text="Поддержка ⚙", url=f"t.me/{settings.bot.SUPPORT_ACCOUNT_USERNAME}")
    ]]
    return InlineKeyboard(inline_keyboard=keyboard)


def manage_user_keyboard(reporter: int, reported: int) -> InlineKeyboard:
    """
    User management keyboard
    """
    builder = InlineBuilder().row(
        InlineButton(
            text="Заблокировать 🔐",
            callback_data=f'{AdminActions.BLOCK}*{reporter}*{reported}'
        )
    )
    return builder.as_markup()
