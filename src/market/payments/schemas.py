from datetime import datetime
from typing import Union

from pydantic import UUID4, BaseModel, Field
from pydantic_extra_types.payment import PaymentCardNumber
from pydantic_extra_types.phone_numbers import PhoneNumber

from market.payments.enums import PaymentDestination, PaymentStatus


class PaymentCredentials(BaseModel):
    destination: PaymentDestination
    account: Union[PhoneNumber, PaymentCardNumber]


class CreatePayment(PaymentCredentials):
    amount: float | int = Field(..., gt=0)
    currency: str


class Payment(BaseModel):
    id: UUID4
    user_id: int
    amount: float | int
    account: str
    currency: str
    destination: PaymentDestination
    created_at: datetime
    status: PaymentStatus
