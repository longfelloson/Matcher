from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.reports.utils import block_user, react_for_report
from bot.users.models import User
from bot.users.schemas import UserActions, AdminActions

router = Router(name="Reports")


@router.callback_query(F.data.regexp(UserActions.REPORT))
async def report_button_handler(call: CallbackQuery, user: User, session: AsyncSession, state: FSMContext):
    """
    Обработка нажатия кнопки "Отправить жалобу"
    """
    await react_for_report(call, user, state, session)


@router.callback_query(F.data.regexp(AdminActions.BLOCK))
async def send_photo_button_handler(call: CallbackQuery, session: AsyncSession):
    """
    Обработка кнопки "Заблокировать пользователя"
    """
    user_id = call.data.split('*')[1]

    await block_user(call.data, session)
    await call.message.edit_text(f"Пользователь <b>#{user_id}</b> заблокирован")
