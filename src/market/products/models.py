import uuid
from sqlalchemy import UUID, Column, Float, String

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    price = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    img_url = Column(String, nullable=False)
