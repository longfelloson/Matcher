from aiogram.filters.callback_data import CallbackData

from bot.adminpanel.users.mailing.enums import MailingAction


class MailingQueryData(CallbackData, prefix="mailing_section_action"):
    action: MailingAction
