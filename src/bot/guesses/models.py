from sqlalchemy import Integer, Column, BigInteger

from database import Base


class Guess(Base):
    __tablename__ = 'guesses'

    guess_id = Column(Integer, primary_key=True, autoincrement=True)
    guesser = Column(BigInteger, nullable=False)
    guessed = Column(BigInteger, nullable=False)
    guessed_at = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
