from pydantic import BaseModel


class Guess(BaseModel):
    guesser: int
    guessed: int
    points: int | float
