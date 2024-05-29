from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Column, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from src.database import Base
from src.users.schemas import UserStatuses


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
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

    config = relationship("UserConfig", uselist=False, backref="users", lazy="selectin")
