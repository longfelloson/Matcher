from pydantic import BaseModel

from bot.users.rates.enums import RateType


class Rate(BaseModel):
    rater_user_id: int
    rated_user_id: int
    type: RateType
