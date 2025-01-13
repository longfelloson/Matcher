from aiogram.utils.keyboard import (
    InlineKeyboardBuilder as InlineBuilder,
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
    ReplyKeyboardBuilder as Builder,
    KeyboardButton as Button,
    ReplyKeyboardMarkup as Keyboard,
)

from bot.keyboards import back_button
from bot.users.enums.actions import UserAction
from bot.users.models import User
from bot.users.rates.constants import USER_RATE_BUTTONS
from bot.users.rates.enums import RateType


def notification_keyboard(rater_id: int) -> InlineKeyboard:
    builder = InlineBuilder().row(
        InlineButton(
            text="Просмотреть 👀",
            callback_data=f"{UserAction.view_rater_user}*{rater_id}",
        )
    )
    return builder.as_markup()


def respond_to_rate_keyboard(user_to_rate: User) -> InlineKeyboard:
    builder = InlineBuilder().row(
        InlineButton(
            text="❤", callback_data=f"rate_user*{RateType.positive}*{user_to_rate.id}"
        ),
        InlineButton(
            text="👎", callback_data=f"rate_user*{RateType.negative}*{user_to_rate.id}"
        ),
    )
    return builder.as_markup()


def rate_buttons_keyboard() -> Keyboard:
    rate_user_buttons = [Button(text=text) for text in USER_RATE_BUTTONS]
    builder = Builder().row(*rate_user_buttons)
    return builder.row(back_button()).as_markup(resize_keyboard=True)
