from sqlalchemy import Column, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database import Base


class UserConfig(Base):
    __tablename__ = 'user_config'

    user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True)
    guess_age = Column(Boolean)

    user = relationship("User", back_populates="config")

