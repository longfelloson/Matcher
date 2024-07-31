from pydantic import BaseModel

from market.transactions.schemas import TransactionType


class ExchangePoints(BaseModel):
    points: int | float
    product_id: int = None
    transaction_type: str = (
        TransactionType.PURCHASE if product_id else TransactionType.EXCHANGE
    )
