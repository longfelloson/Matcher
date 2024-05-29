from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String

from src.database import Base


class Rate(Base):
    __tablename__ = 'rates'

    rate_id = Column(Integer, primary_key=True, autoincrement=True)
    rater = Column(Integer, nullable=False)
    rated = Column(Integer, nullable=False)
    rated_at = Column(DateTime, nullable=False, default=datetime.now())
    rate_type = Column(String, nullable=False)
