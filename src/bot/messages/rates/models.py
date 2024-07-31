from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, BigInteger

from database import Base


class Rate(Base):
    __tablename__ = "rates"

    rate_id = Column(Integer, primary_key=True, autoincrement=True)
    rater = Column(BigInteger, nullable=False)
    rated = Column(BigInteger, nullable=False)
    rated_at = Column(DateTime, nullable=False, default=datetime.now())
    rate_type = Column(String, nullable=False)
