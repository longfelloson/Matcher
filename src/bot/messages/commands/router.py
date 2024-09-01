from typing import Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.adminpanel.keyboards import admin_panel_keyboard
from bot.keyboards import main_keyboard, help_command_keyboard
from bot.messages.enums import Answer
from bot.messages.registration.schemas import Answer as RegistrationAnswers, RegistrationSectionAnswer
from bot.messages.registration.states import RegistrationStates
from bot.users import crud as users_crud
from bot.users.models import User
from bot.users.utils import get_user_schema_from_message

router = Router(name="Commands")


@router.message(Command("start"))
async def command_start_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: Optional[User]
):
    if not user:
        await users_crud.create_user(get_user_schema_from_message(message), session)
        await state.set_state(RegistrationStates.age)
        await message.answer(RegistrationSectionAnswer.age)
    else:
        await message.answer(Answer.greeting, reply_markup=main_keyboard())


@router.message(Command("help"))
async def command_help_handler(message: Message):
    await message.answer(Answer.help_command, reply_markup=help_command_keyboard())


@router.message(Command("admin"))
async def command_help_handler(message: Message):
    await message.answer(Answer.admin_command, reply_markup=admin_panel_keyboard())
