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

from bot.adminpanel.enums import AdminAction
from config import settings
from market.auth.token import get_auth_link


def main_keyboard() -> Keyboard:
    """
    Клавиатура для главного меню
    """
    builder = Builder().row(Button(text="Начать ▶️"))
    builder.row(Button(text="Профиль 📱"))
    #  builder.row(Button(texts="Магазин 🛍"))
    return builder.as_markup(resize_keyboard=True)


def help_command_keyboard() -> InlineKeyboard:
    """
    Клавиатура ответа на команду вызова поддержки
    """
    keyboard = [
        [
            InlineButton(
                text="Поддержка ⚙", url=f"t.me/{settings.BOT.SUPPORT_ACCOUNT_USERNAME}"
            )
        ]
    ]
    return InlineKeyboard(inline_keyboard=keyboard)


def manage_user_keyboard(reporter: int, reported: int) -> InlineKeyboard:
    """
    Клавиатура управления пользователем
    """
    builder = InlineBuilder().row(
        InlineButton(
            text="Заблокировать 🔐",
            callback_data=f"{AdminAction.ban_user}*{reporter}*{reported}",
        )
    )
    return builder.as_markup()


def market_link_keyboard(user_id: int) -> InlineKeyboard:
    """
    Клавиатура из одной кнопки, содержащую ссылку на маркет
    """
    link_with_auth_token = get_auth_link(user_id)
    builder = InlineBuilder().row(
        InlineButton(
            text="🔗",
            web_app=WebAppInfo(url=settings.MARKET.MARKET_LINK + link_with_auth_token),
        )
    )
    return builder.as_markup()
