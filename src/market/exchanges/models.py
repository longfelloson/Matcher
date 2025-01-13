from datetime import datetime
import uuid
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Float,
)
from sqlalchemy.types import UUID
from database import Base


class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    payment_id = Column(
        UUID(as_uuid=True), ForeignKey("payments.id"), nullable=False
    )
    points = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
