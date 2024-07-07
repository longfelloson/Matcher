from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):
    __tablename__ = "products"

    id_ = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    img_path = Column(String, nullable=False)


class UserProduct(Base):
    __tablename__ = "user_products"

    id_ = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id_"), nullable=False)

    product = relationship("Product", lazy="selectin")
