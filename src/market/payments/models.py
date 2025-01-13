from datetime import datetime
import uuid

from sqlalchemy import UUID, BigInteger, Column, Float, Integer, String, DateTime, ForeignKey

from database import Base
from market.payments.enums import PaymentStatus


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    account = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String, default=PaymentStatus.completed)
