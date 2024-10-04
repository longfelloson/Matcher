from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.adminpanel.users.enums import Action
from bot.adminpanel.users.schemas import UsersSectionAction
from bot.loader import bot
from bot.users import crud
from bot.users.enums.statuses import UserStatus

router = Router()


@router.callback_query(UsersSectionAction.filter(F.action == Action.block))
async def block_user(
        query: CallbackQuery,
        callback_data: UsersSectionAction,
        session: AsyncSession,
):
    await bot.answer_callback_query(query.id)

    await crud.update_user(callback_data.user_id, session, status=UserStatus.blocked)
    await query.message.edit_text(f"Пользователь {callback_data.user_id} заблокирован!")


@router.callback_query(UsersSectionAction.filter(F.action == Action.view_users_amount))
async def view_users_amount(query: CallbackQuery, session: AsyncSession):
    await bot.answer_callback_query(query.id)

    users_amount = await crud.get_users_amount(session)
    await query.message.edit_text(f"Всего пользователей: {users_amount}")
