from pydantic import BaseModel


class UserConfig(BaseModel):
    """
    Конфигурация пользователя
    """
    user_id: int
    guess_age: bool
