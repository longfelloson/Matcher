from datetime import datetime

from sqlalchemy import String, DateTime, Column, Float, Integer, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from bot.users.schemas import UserStatuses
from database import Base


class UserConfig(Base):
    __tablename__ = 'user_config'

    user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True)
    guess_age = Column(Boolean)

    user = relationship("User", back_populates="config")


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    username = Column(String, nullable=True)
    status = Column(String, default=UserStatuses.NOT_REGISTERED)
    created_at = Column(DateTime, default=datetime.now)
    instagram = Column(String, nullable=True)
    age = Column(Integer)
    gender = Column(String, nullable=True)
    preferred_gender = Column(String, nullable=True)
    preferred_age_group = Column(String)
    location = Column(String, nullable=True)
    city = Column(String, nullable=True)
    photo_file_id = Column(String, nullable=True)
    points = Column(Float, default=0.0)

    config = relationship("UserConfig", back_populates="user", uselist=False, lazy="selectin")
