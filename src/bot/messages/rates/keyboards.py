from aiogram.utils.keyboard import (
    InlineKeyboardBuilder as InlineBuilder,
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
)

from bot.messages.rates.enums import RateType
from bot.users.enums import UserAction
from bot.users.models import User


def notification_keyboard(rater_id: int) -> InlineKeyboard:
    builder = InlineBuilder().row(
        InlineButton(
            text="Просмотреть 👀",
            callback_data=f"{UserAction.view_rater_user.value}*{rater_id}"
        )
    )
    return builder.as_markup()


def respond_to_rate_keyboard(user_to_rate: User) -> InlineKeyboard:
    builder = InlineBuilder().row(
        InlineButton(
            text="❤",
            callback_data=f"rate_user*{RateType.positive}*{user_to_rate.user_id}"
        ),
        InlineButton(
            text="👎",
            callback_data=f"rate_user*{RateType.negative}*{user_to_rate.user_id}"
        ),
    )
    return builder.as_markup()
