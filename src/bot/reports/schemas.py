from pydantic import BaseModel

from bot.reports.enums import ReportStatus


class Report(BaseModel):
    id: int
    reporter: int
    reported: int
    reported_at: int
    status: ReportStatus.PENDING
