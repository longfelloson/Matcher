from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.adminpanel.users.mailing.states import MailingState

mailing_router = Router(name="Maling router")


@mailing_router.message(MailingState.text, F.content_type == ContentType.TEXT)
async def get_text_for_mailing(message: Message, state: FSMContext):
    await state.update_data(text_for_mailing=message.text)
    await message.answer("Выберите действие ")