from aiogram.filters.callback_data import CallbackData

from bot.adminpanel.users.mailing.enums import MailingSectionAction


class MailingQueryData(CallbackData, prefix="mailing_section_action"):
    action: MailingSectionAction
