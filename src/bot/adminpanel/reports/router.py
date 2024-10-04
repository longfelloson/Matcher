from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.adminpanel.reports import utils
from bot.adminpanel.reports.enums import ReportAction
from bot.adminpanel.reports.schemas import ReportsSectionAction
from bot.loader import bot
from bot.reports import crud

router = Router()


@router.callback_query(ReportsSectionAction.filter(F.action == ReportAction.APPROVE))
async def approve_report(
        query: CallbackQuery,
        query_data: ReportsSectionAction,
        session: AsyncSession,
):
    report = await crud.get_report(query_data.report_id, session)

    await bot.answer_callback_query(query.id)
    await utils.approve_report(report, session)


@router.callback_query(ReportsSectionAction.filter(F.action == ReportAction.DECLINE))
async def decline_report(
        query: CallbackQuery,
        query_data: ReportsSectionAction,
        session: AsyncSession,
):
    report = await crud.get_report(query_data.report_id, session)

    await bot.answer_callback_query(query.id)
    await utils.decline_report(report, session)
