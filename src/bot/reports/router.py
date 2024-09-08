from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.adminpanel.enums import AdminAction
from bot.reports import crud
from bot.reports.utils import approve_report, decline_report

router = Router(name="Reports")


@router.callback_query(F.data.regexp(AdminAction.approve_report))
async def approve_report_button_handler(call: CallbackQuery, session: AsyncSession):
    report_id = call.data.split("*")[1]
    report = await crud.get_report(report_id, session)

    await approve_report(report, session)
    await call.message.delete()
    await call.answer("Пользователь заблокирован ✔️", show_alert=True)


@router.callback_query(F.data.regexp(AdminAction.decline_report))
async def decline_report_button_handler(call: CallbackQuery, session: AsyncSession):
    report_id = call.data.split("*")[1]
    report = await crud.get_report(report_id, session)

    await decline_report(report, session)
    await call.message.delete()
    await call.answer("Жалоба отклонена ✔️", show_alert=True)
