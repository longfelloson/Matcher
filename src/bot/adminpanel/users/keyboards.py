from aiogram.utils.keyboard import (
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
    InlineKeyboardBuilder as InlineBuilder,
)

from bot.adminpanel.users.enums import Action, ActionName
from bot.adminpanel.users.schemas import UsersSectionAction


def users_section_actions_keyboard() -> InlineKeyboard:
    buttons = [
        InlineButton(
            text=action_name, callback_data=UsersSectionAction(action=action).pack()
        )
        for action_name, action in zip(ActionName, Action)
    ]
    return InlineBuilder().add(*buttons).adjust(1).as_markup()
