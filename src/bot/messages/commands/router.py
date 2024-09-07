from typing import Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.adminpanel.keyboards import admin_panel_keyboard
from bot.filters import UserAdminFilter
from bot.keyboards import main_keyboard, help_command_keyboard
from bot.messages.commands.enums import CommandAnswer
from bot.messages.registration.enums.answers import RegistrationSectionAnswer
from bot.messages.registration.states import RegistrationStates
from bot.reports.utils import react_for_report
from bot.users import crud as users_crud
from bot.users.models import User
from bot.users.utils import get_user_schema_from_message, send_user_to_react

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
        await message.answer(CommandAnswer.start, reply_markup=main_keyboard())


@router.message(Command("help"))
async def command_help_handler(message: Message):
    await message.answer(CommandAnswer.help, reply_markup=help_command_keyboard())


@router.message(UserAdminFilter(), Command("admin"))
async def command_help_handler(message: Message):
    await message.answer(CommandAnswer.admin, reply_markup=admin_panel_keyboard())


@router.message(Command("report"))
async def report_command_handler(
    message: Message,
    user: User,
    state: FSMContext,
    session: AsyncSession,
):
    """Обработка команды 'report'"""
    state_data = await state.get_data()
    reported_user = state_data.get("user_for_rate")
    if not reported_user:
        await message.answer(CommandAnswer.no_reported)
    else:
        await react_for_report(message, user.user_id, reported_user.user_id, session)
        await send_user_to_react(message, user, session, state)
