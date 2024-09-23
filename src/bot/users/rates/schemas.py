from pydantic import BaseModel


class Rate(BaseModel):
    rater: int
    rated: int
    rate_type: str
