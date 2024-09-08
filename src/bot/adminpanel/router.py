from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.adminpanel import actions
from bot.adminpanel.enums import AdminAction, AdminPanelSection
from bot.adminpanel.keyboards import stats_section_keyboard

router = Router()


@router.callback_query(F.data.regexp("admin_action"))
async def admin_action_button_handler(call: CallbackQuery, session: AsyncSession):
    """
    Обработка кнопок действий админа в админпанели
    """
    action = call.data.split("*")[1]
    user_id = None if len(call.data.split("*")) >= 2 else call.data.split("*")[2]

    match action:
        case AdminAction.ban_user:
            await actions.ban_user(call.message, user_id, session)
        case AdminAction.unban_user:
            await actions.unban_user(call.message, user_id, session)
        case AdminAction.view_users_amount:
            await actions.view_users_amount(call.message, session)


@router.callback_query(F.data.regexp("admin_panel_section"))
async def view_section_button_handler(call: CallbackQuery):
    """Обработка кнопок просмотра отдела в админ панели"""
    section = call.data.split("*")[1]
    match section:
        case AdminPanelSection.stats:
            await call.message.edit_text("Выберите действие", reply_markup=stats_section_keyboard())
