from datetime import datetime

from sqlalchemy import Column, Integer, DateTime


class Report:
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    reporter = Column(Integer, nullable=False)
    reported = Column(Integer, nullable=False)
    reported_at = Column(DateTime, nullable=False, default=datetime.now())
