from aiogram.types import (
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder as InlineBuilder

from bot.reports.models import Report


def report_manage_keyboard(report: Report) -> InlineKeyboard:
    builder = InlineBuilder().row(
        InlineButton(
            text="Заблокировать ✔️",
            callback_data=f"approve_report*{report.report_id}"
        )
    )
    builder.row(
        InlineButton(
            text="Отклонить ❌ ",
            callback_data=f"decline_report*{report.report_id}"
        )
    )
    return builder.as_markup()
