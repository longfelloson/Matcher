from typing import Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard, help_command_keyboard
from bot.messages.registration.schemas import Answers as RegistrationAnswers
from bot.messages.registration.states import RegistrationStates
from bot.messages.schemas import Answers
from bot.users import crud as users_crud
from bot.users.models import User
from bot.users.schemas import get_user_schema_from_message

router = Router(name='Commands')


@router.message(Command('start'))
async def command_start_handler(message: Message, session: AsyncSession, state: FSMContext, user: Optional[User]):
    """
    Обработка команды "/start"
    """
    if not user:
        await users_crud.create_user(get_user_schema_from_message(message), session)
        await state.set_state(RegistrationStates.age)
        await message.answer(RegistrationAnswers.USER_AGE_SECTION)
    else:
        await message.answer(Answers.GREETING, reply_markup=main_keyboard())


@router.message(Command('help'))
async def command_help_handler(message: Message):
    """
    Обработка команды "/help"
    """
    await message.answer(Answers.HELP_COMMAND, reply_markup=help_command_keyboard())


@router.message(Command('admin'))
async def command_help_handler(message: Message):
    """
    Обработка команды "/admin"
    """
    await message.answer(Answers.ADMIN_COMMAND)
