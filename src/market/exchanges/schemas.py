from datetime import datetime
from pydantic import UUID4, BaseModel

from market.payments.schemas import CreatePayment


class Exchange(BaseModel):
    id: UUID4
    payment_id: UUID4
    user_id: int
    created_at: datetime
    rate: int | float
    points: int | float


class CreateExchange(CreatePayment):
    points: int | float
    rate: int | float
