from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.reports.models import Report
from src.reports.schemas import Report as ReportSchema


async def add_report(report: ReportSchema, session: AsyncSession):
    """
    Добавление жалобы в базу
    """
    await session.execute(insert(Report).values(**report.model_dump()))
    await session.commit()
