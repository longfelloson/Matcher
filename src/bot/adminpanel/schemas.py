from aiogram.filters.callback_data import CallbackData

from bot.adminpanel.enums import Section


class SectionQueryData(CallbackData, prefix="view_admin_panel_section"):
    section: Section
