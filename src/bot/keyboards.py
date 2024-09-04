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

from config import settings


def main_keyboard() -> Keyboard:
    """
    Клавиатура для главного меню
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
    Клавиатура ответа на команду вызова поддержки
    """
    keyboard = [
        [
            InlineButton(
                text="Поддержка ⚙", url=f"t.me/{settings.SUPPORT_ACCOUNT_USERNAME}"
            )
        ]
    ]
    return InlineKeyboard(inline_keyboard=keyboard)


def market_link_keyboard(link: str) -> InlineKeyboard:
    """
    Клавиатура из одной кнопки, содержащую ссылку на маркет
    """
    builder = InlineBuilder().row(
        InlineButton(
            text="🔗",
            web_app=WebAppInfo(url=settings.MARKET_LINK + link),
        )
    )
    return builder.as_markup()
