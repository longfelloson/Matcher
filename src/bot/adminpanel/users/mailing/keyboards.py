from aiogram.utils.keyboard import (
    InlineKeyboardBuilder as InlineBuilder,
    InlineKeyboardButton as InlineButton,
    InlineKeyboardMarkup as InlineKeyboard,
)

from bot.adminpanel.users.mailing.enums import MailingAction
from bot.adminpanel.users.mailing.schemas import MailingQueryData

ONE_BUTTON_PER_ROW = 1


def mailing_action() -> InlineKeyboard:
    buttons = [
        InlineButton(
            text=action.name, callback_data=MailingQueryData(action=action)
        )
        for action in MailingAction
    ]
    return InlineBuilder().add(*buttons).adjust(ONE_BUTTON_PER_ROW)
