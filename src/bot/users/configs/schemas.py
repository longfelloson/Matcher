from pydantic import BaseModel


class UserConfig(BaseModel):
    user_id: int
    guess_age: bool
