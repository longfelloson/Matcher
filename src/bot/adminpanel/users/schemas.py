from aiogram.filters.callback_data import CallbackData

from bot.adminpanel.users.enums import Action


class UsersSectionAction(CallbackData, prefix="users_section_action"):
    action: Action
