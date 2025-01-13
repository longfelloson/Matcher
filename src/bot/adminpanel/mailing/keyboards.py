from aiogram.utils.keyboard import (
    InlineKeyboardBuilder as InlineBuilder,
    InlineKeyboardButton as InlineButton,
    InlineKeyboardMarkup as InlineKeyboard,
)

from bot.adminpanel.mailing.enums import MailingAction
from bot.adminpanel.mailing.schemas import MailingQueryData
from bot.constants import ONE_BUTTON_IN_ROW


def mailing_action_keyboard() -> InlineKeyboard:
    buttons = [
        InlineButton(text=action.name, callback_data=MailingQueryData(action=action))
        for action in MailingAction
    ]
    return InlineBuilder().add(*buttons).adjust(ONE_BUTTON_IN_ROW).as_markup()
