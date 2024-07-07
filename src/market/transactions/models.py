from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id_ = Column(Integer, primary_key=True)
    type_ = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id_'), nullable=True)
