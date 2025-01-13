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

from bot.constants import BACK_BUTTON_EMOJI, ONE_BUTTON_IN_ROW
from config import settings


def main_keyboard() -> Keyboard:
    buttons_texts = ["Начать ▶️", "Профиль 📱", "Магазин 🛍"]
    buttons = [Button(text=button_text) for button_text in buttons_texts]
    return (
        Builder()
        .add(*buttons)
        .adjust(ONE_BUTTON_IN_ROW)
        .as_markup(resize_keyboard=True)
    )


def help_command_keyboard() -> InlineKeyboard:
    buttons = [
        InlineButton(
            text="Поддержка ⚙", url=f"t.me/{settings.SUPPORT_ACCOUNT_USERNAME}"
        )
    ]
    return InlineBuilder().add(*buttons).as_markup()


def market_link_keyboard(link: str) -> InlineKeyboard:
    buttons = [
        InlineButton(
            text="🔗",
            web_app=WebAppInfo(url=settings.MARKET_LINK + link),
        ),
    ]
    return InlineBuilder().add(*buttons).as_markup()


def back_button(as_builder: bool = False) -> Builder | Keyboard:
    """Returns Keyboard or Builder with back button"""
    button = Button(text=BACK_BUTTON_EMOJI)
    if as_builder:
        return Builder().add(button)

    return button
