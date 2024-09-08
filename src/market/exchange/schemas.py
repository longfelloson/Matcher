from pydantic import BaseModel

from market.transactions.enums import TransactionType


class ExchangePoints(BaseModel):
    points: int | float
    product_id: int = None
    transaction_type: str = (
        TransactionType.purchase if product_id else TransactionType.exchange
    )
