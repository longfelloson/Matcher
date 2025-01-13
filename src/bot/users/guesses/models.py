from datetime import datetime

from sqlalchemy import Integer, Column, BigInteger, DateTime

from database import Base


class Guess(Base):
    __tablename__ = "guesses"

    id = Column(Integer, primary_key=True)
    guesser_user_id = Column(BigInteger, nullable=False)
    guessed_user_id = Column(BigInteger, nullable=False)
    guessed_at = Column(DateTime, nullable=False, default=datetime.now)
    points = Column(Integer, nullable=False)
