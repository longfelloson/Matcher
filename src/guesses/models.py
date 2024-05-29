from sqlalchemy import Integer, Column

from src.database import Base


class Guess(Base):
    __tablename__ = 'guesses'

    guess_id = Column(Integer, primary_key=True, autoincrement=True)
    guesser = Column(Integer, nullable=False)
    guessed = Column(Integer, nullable=False)
    guessed_at = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
