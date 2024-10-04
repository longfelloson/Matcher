from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from bot.adminpanel.reports.enums import ReportAction


class ReportsSectionAction(CallbackData, prefix="reports_section_action"):
    action: ReportAction
    report_id: UUID4
