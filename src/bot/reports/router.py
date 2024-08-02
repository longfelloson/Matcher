from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.adminpanel.enums import AdminAction
from bot.reports.utils import block_user, react_for_report
from bot.users.enums import UserAction
from bot.users.models import User

router = Router(name="Reports")


@router.callback_query(F.data.regexp(UserAction.report_user))
async def report_button_handler(
        call: CallbackQuery, user: User, session: AsyncSession, state: FSMContext
):
    """
    Обработка нажатия кнопки "Отправить жалобу"
    """
    await react_for_report(call, user, state, session)


@router.callback_query(F.data.regexp(AdminAction.ban_user))
async def ban_user(call: CallbackQuery, session: AsyncSession):
    """
    Обработка кнопки "Заблокировать пользователя"
    """
    user_id = call.data.split("*")[1]

    await block_user(call.data, session)
    await call.message.edit_text(f"Пользователь <b>#{user_id}</b> заблокирован")
