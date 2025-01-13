from datetime import datetime
from pydantic import UUID4, BaseModel


class PurchaseBase(BaseModel):
    product_id: UUID4
    amount: float | int


class CreatePurchase(PurchaseBase): ...


class Purchase(PurchaseBase):
    id: UUID4
    created_at: datetime
    user_id: int
