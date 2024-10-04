from aiogram.utils.keyboard import (
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
    InlineKeyboardBuilder as InlineBuilder,
)

from bot.adminpanel.reports.enums import ReportAction
from bot.adminpanel.reports.schemas import ReportsSectionAction

from bot.reports.models import Report


def report_manage_keyboard(report: Report) -> InlineKeyboard:
    builder = InlineBuilder().row(
        InlineButton(
            text="Заблокировать ✔️",
            callback_data=ReportsSectionAction(action=ReportAction.APPROVE, report_id=report.report_id).pack()
        )
    )
    builder.row(
        InlineButton(
            text="Отклонить ❌",
            callback_data=ReportsSectionAction(action=ReportAction.DECLINE, report_id=report.report_id).pack()
        )
    )
    return builder.as_markup()
