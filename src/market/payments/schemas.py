from typing import Union

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic_extra_types.payment import PaymentCardNumber

from market.payments.enums import PaymentDestination


class PaymentCredentials(BaseModel):
    destination: PaymentDestination
    account: Union[PhoneNumber, PaymentCardNumber]


class CreatePayment(PaymentCredentials):
    amount: Union[float, int]
    sbp_bank_id: int
    amount: float
    payment_system_id: int
