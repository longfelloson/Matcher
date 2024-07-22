from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from database import Base


class Payment(Base):
    __tablename__ = 'payments'

    id_ = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    amount = Column(Integer, nullable=False)
    account = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
