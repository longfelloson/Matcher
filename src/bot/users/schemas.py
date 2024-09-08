from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: Optional[str]
