from pydantic import BaseModel


class PaymentCredentials(BaseModel):
    destination: str
    account: str


class CreatePayment(PaymentCredentials):
    user_id: int
    amount: float | int
    currency: str


class PaymentStatus:
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'


class WithdrawPaymentData(BaseModel):
    ...
