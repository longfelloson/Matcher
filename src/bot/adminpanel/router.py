from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.adminpanel import actions
from bot.adminpanel.enums import AdminAction

router = Router()


@router.callback_query(F.data.regexp("admin_action"))
async def admin_action_button_handler(call: CallbackQuery, session: AsyncSession):
    """
    Обработка кнопок действий админа в админпанели
    """
    action, user_id = call.data.split("*")[1:]

    match action:
        case AdminAction.ban_user:
            await actions.ban_user(call.message, user_id, session)
        case AdminAction.unban_user:
            await actions.unban_user(call.message, user_id, session)
