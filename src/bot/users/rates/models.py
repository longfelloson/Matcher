from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    BigInteger,
)

from database import Base


class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True)
    rater_user_id = Column(BigInteger, nullable=False)
    rated_user_id = Column(BigInteger, nullable=False)
    rated_at = Column(DateTime, nullable=False, default=datetime.now)
    type = Column(String, nullable=False)
