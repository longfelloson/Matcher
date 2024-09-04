from typing import Union

from pydantic import BaseModel


class Guess(BaseModel):
    guesser: int
    guessed: int
    points: Union[int, float]
