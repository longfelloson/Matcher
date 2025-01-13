from enum import StrEnum


class PaymentStatus(StrEnum):
    pending = "PENDING"
    completed = "COMPLETED"


class PaymentDestination(StrEnum):
    tbank = "tbank"
    sberbank = "sberbank"


class PaymentCurrency(StrEnum):
    EUR = "EUR"
    USD = "USD"
    