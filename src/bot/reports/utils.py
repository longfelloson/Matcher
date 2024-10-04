import asyncio
from typing import Union

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.adminpanel.reports.keyboards import report_manage_keyboard
from bot.reports import crud
from bot.reports.enums import Answer
from bot.reports.models import Report
from bot.reports.schemas import Report as ReportSchema
from bot.texts.users import get_user_link
from bot.users import crud as users_crud
from bot.users.enums.statuses import UserStatus
from bot.users.models import User
from bot.users.utils import send_user_to_view
from config import settings

DEFAULT_DELAY = 0.75


async def react_for_report(
        message: Message,
        reporter_user_id: Union[str, int],
        reported_user_id: Union[str, int],
        session: AsyncSession,
) -> None:
    report = Report(reporter=reporter_user_id, reported=reported_user_id)
    reported_user = await users_crud.get_user(report.reported, session)

    await crud.add_report(report, session)
    await users_crud.update_user(reported_user_id, session, status=UserStatus.reported)

    answer_to_report = await message.answer(Answer.sent_report)

    await asyncio.sleep(DEFAULT_DELAY)
    await answer_to_report.delete()

    await send_reported_user_to_moderators(report, reported_user)


async def send_reported_user_to_moderators(report: ReportSchema, reported: User):
    for admin_id in settings.admins_ids:
        reported_link = get_user_link(reported)
        reported_info = f"{reported.name} {reported_link}"

        await send_user_to_view(
            photo=reported.photo_url,
            caption=reported_info,
            keyboard=report_manage_keyboard(report),
            chat_id=admin_id
        )
