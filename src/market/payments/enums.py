from enum import Enum


class PaymentStatus(Enum):
    pending = "PENDING"
    completed = "COMPLETED"


class PaymentDestination(Enum):
    tbank = "tbank"
