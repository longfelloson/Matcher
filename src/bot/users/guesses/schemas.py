from pydantic import BaseModel


class Guess(BaseModel):
    guesser_user_id: int
    guessed_user_id: int
    points: int | float
