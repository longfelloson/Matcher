from sqlalchemy import Integer, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from src.database import Base
from src.users.models import User


class UserConfig(Base):
    __tablename__ = 'user_config'

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    guess_age = Column(Boolean)

    user = relationship("User", back_populates="config")
