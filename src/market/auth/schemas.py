from pydantic import BaseModel


class User(BaseModel):
    id: int
    points: float | int
