from aiogram.types import ReplyKeyboardMarkup as Keyboard, KeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup as InlineKeyboard, InlineKeyboardButton as InlineButton
from aiogram.utils.keyboard import InlineKeyboardBuilder as InlineBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from src import config
from src.users.schemas import AdminActions, User


def main_keyboard() -> Keyboard:
    """
    Главная клавиатура
    """
    builder = Builder().row(
        Button(text="Начать")
    )
    builder.row(
        Button(text="Профиль")
    )
    builder.row(
        Button(text="Магазин")
    )
    return builder.as_markup(resize_keyboard=True)


def help_command_keyboard() -> InlineKeyboard:
    """
    Клавиатура ответного сообщения на команду "/help"
    """
    keyboard = [[
        InlineButton(text="Поддержка ⚙", url=f"t.me/{config.SUPPORT_ACCOUNT_USERNAME}")
    ]]
    return InlineKeyboard(inline_keyboard=keyboard)


def manage_user_keyboard(reporter: int, reported: int) -> InlineKeyboard:
    """

    """
    builder = InlineBuilder().row(
        InlineButton(
            text="Заблокировать 🔐",
            callback_data=f'{AdminActions.BLOCK}*{reporter}*{reported}'
        )
    )
    return builder.as_markup()
