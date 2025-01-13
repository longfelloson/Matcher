from datetime import datetime
from pydantic import UUID4, BaseModel


class Exchange(BaseModel):
    id: UUID4
    payment_id: UUID4
    user_id: int
    created_at: datetime
    rate: int | float
    points: int | float


class CreateExchange(BaseModel):
    rate: int | float
    points: int | float
    payment_id: UUID4
