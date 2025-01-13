from datetime import datetime
import uuid
from sqlalchemy import UUID, BigInteger, Column, DateTime, Float, ForeignKey, Integer
from database import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    product_id = Column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
