from typing import Union

from pydantic import UUID4
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.reports.models import Report
from bot.reports.schemas import Report as ReportSchema


async def get_report(report_id: Union[UUID4, str], session: AsyncSession) -> Report:
    report = await session.execute(select(Report).where(Report.report_id == report_id))
    return report.scalar_one()


async def add_report(report: ReportSchema, session: AsyncSession) -> None:
    await session.execute(insert(Report).values(**report.model_dump()))
    await session.commit()


async def update_report(
    report_id: Union[UUID4, str],
    session: AsyncSession,
    **values,
) -> None:
    await session.execute(update(Report).values(**values).where(Report.report_id == report_id))
    await session.commit()
