from sqlalchemy.ext.asyncio import AsyncSession

from bot.reports import crud
from bot.reports.enums import ReportStatus
from bot.reports.schemas import Report as ReportSchema
from bot.users import crud as users_crud
from bot.users.enums.statuses import UserStatus
from config import settings


async def approve_report(report: ReportSchema, session: AsyncSession) -> None:
    """Блокировка пользователя и начисление баллов за корректную жалобу"""
    await users_crud.update_user(report.reported, session, status=UserStatus.blocked)
    await users_crud.increase_user_points(report.reporter, settings.POINTS_FOR_BLOCKED_USER, session)
    await crud.update_report(report.report_id, session, status=ReportStatus.APPROVED)


async def decline_report(report: ReportSchema, session: AsyncSession) -> None:
    """Отклонение пользовательской жалобы"""
    await users_crud.update_user(report.reported, session, status=UserStatus.active)
    await crud.update_report(report.report_id, session, status=ReportStatus.DECLINED)
