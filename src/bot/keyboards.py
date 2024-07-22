from aiogram.types import (
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
    WebAppInfo,
)
from aiogram.types import (
    ReplyKeyboardMarkup as Keyboard,
    KeyboardButton as Button,
)
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder as InlineBuilder,
    ReplyKeyboardBuilder as Builder,
)

from bot.users.schemas import AdminActions
from config import settings
from market.auth.token import get_link_with_token


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
    builder.row(
        Button(text="Магазин 🛍")
    )
    return builder.as_markup(resize_keyboard=True)


def help_command_keyboard() -> InlineKeyboard:
    """
    Help's command keyboard
    """
    keyboard = [[
        InlineButton(text="Поддержка ⚙", url=f"t.me/{settings.BOT.SUPPORT_ACCOUNT_USERNAME}")
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


def market_link_keyboard(user_id: int) -> InlineKeyboard:
    """
    Button with market auth link
    """
    link_with_auth_token = get_link_with_token(user_id)
    builder = InlineBuilder().row(
        InlineButton(text="🔗", web_app=WebAppInfo(url=settings.MARKET_LINK + link_with_auth_token))
    )
    return builder.as_markup()
