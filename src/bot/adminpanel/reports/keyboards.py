from aiogram.utils.keyboard import (
    InlineKeyboardMarkup as InlineKeyboard,
    InlineKeyboardButton as InlineButton,
    InlineKeyboardBuilder as InlineBuilder,
)

from bot.adminpanel.reports.enums import ReportAction
from bot.adminpanel.reports.schemas import ReportsSectionAction
from bot.constants import ONE_BUTTON_IN_ROW
from bot.reports.models import Report


def report_manage_keyboard(report: Report) -> InlineKeyboard:
    buttons = [
        InlineButton(
            text="Заблокировать ✔️",
            callback_data=ReportsSectionAction(
                action=ReportAction.APPROVE, report_id=report.id
            ).pack(),
        ),
        InlineButton(
            text="Отклонить ❌",
            callback_data=ReportsSectionAction(
                action=ReportAction.DECLINE, report_id=report.id
            ).pack(),
        ),
    ]
    return InlineBuilder().add(*buttons).adjust(ONE_BUTTON_IN_ROW).as_markup()
