from typing import Optional

from aiogram import Router, F
from aiogram.filters import Command, or_f, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.adminpanel.keyboards import select_section_keyboard
from bot.captcha.utils import send_captcha, generate_captcha
from bot.keyboards import main_keyboard, help_command_keyboard
from bot.messages.commands.enums import CommandAnswer
from bot.texts.utils import spoiler
from bot.users.models import User
from config import settings

router = Router(name="Commands")


@router.message(or_f(CommandStart(), F.text == "↩"))
async def start_command_handler(
        message: Message,
        state: FSMContext,
        user: Optional[User]
):
    if not user:
        user_id = message.chat.id

        captcha = generate_captcha()
        hidden_correct_emoji = spoiler(captcha["correct_emoji"])

        await send_captcha(user_id, captcha["emojis"], hidden_correct_emoji)
    else:
        await state.clear()
        await message.answer(CommandAnswer.start, reply_markup=main_keyboard())


@router.message(Command("help"))
async def help_command_handler(message: Message):
    await message.answer(CommandAnswer.help, reply_markup=help_command_keyboard())


@router.message(Command("admin"), F.from_user.id.in_(settings.admins_ids))
async def admin_command_handler(message: Message):
    await message.answer(CommandAnswer.admin, reply_markup=select_section_keyboard())
