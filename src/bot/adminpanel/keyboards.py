from aiogram.types import (
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder as InlineBuilder

from bot.adminpanel.enums import AdminPanelSection, AdminAction


def admin_panel_keyboard() -> InlineKeyboard:
    builder = InlineBuilder().row(
        InlineButton(
            text="Статистика",
            callback_data=f"admin_panel_section*{AdminPanelSection.stats.value}"
        ),
        InlineButton(
            text="Пользователи",
            callback_data=f"admin_panel_section*{AdminPanelSection.stats.value}"
        ),
    )
    return builder.as_markup()


def stats_section_keyboard() -> InlineKeyboard:
    builder = InlineBuilder().row(
        InlineButton(
            text="Все пользователи",
            callback_data=f"admin_action*{AdminAction.view_users_amount.value}"
        )
    )
    return builder.as_markup()
