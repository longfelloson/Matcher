from aiogram.utils.keyboard import (
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
    InlineKeyboardBuilder as InlineBuilder,
)

from bot.adminpanel.enums import SectionName, Section
from bot.adminpanel.schemas import SectionQueryData


def select_section_keyboard() -> InlineKeyboard:
    buttons = [
        InlineButton(
            text=section_name, callback_data=SectionQueryData(section=section).pack()
        )
        for section_name, section in zip(SectionName, Section)
    ]
    return InlineBuilder().add(*buttons).as_markup()
