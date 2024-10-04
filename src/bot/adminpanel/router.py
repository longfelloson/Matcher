from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.adminpanel.enums import Section
from bot.adminpanel.reports.router import router as reports_router
from bot.adminpanel.schemas import SectionQueryData
from bot.adminpanel.users.keyboards import users_section_actions_keyboard
from bot.adminpanel.users.router import router as users_router
from bot.loader import bot

router = Router()
router.include_router(reports_router)
router.include_router(users_router)


@router.callback_query(SectionQueryData.filter(F.section == Section.users))
async def view_users_section(query: CallbackQuery):
    await bot.answer_callback_query(query.id)
    await query.message.edit_text(
        text="Выберите действие или раздел ⤵️", reply_markup=users_section_actions_keyboard()
    )
