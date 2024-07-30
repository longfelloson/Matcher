from pydantic import BaseModel


class PaymentCredentials(BaseModel):
    destination: str
    account: str


class CreatePayment(PaymentCredentials):
    amount: float | int
    sbp_bank_id: int
    amount: float
    payment_system_id: int


class PaymentStatus:
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
