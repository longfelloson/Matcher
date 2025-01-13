from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    DateTime,
    String,
)

from bot.reports.enums import ReportStatus
from database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    reporter = Column(BigInteger, nullable=False)
    reported = Column(BigInteger, nullable=False)
    reported_at = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(String, nullable=False, default=ReportStatus.PENDING)
