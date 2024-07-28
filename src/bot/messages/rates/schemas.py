from pydantic import BaseModel


class RateType:
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"


class Rate(BaseModel):
    rater: int
    rated: int
    rate_type: str
