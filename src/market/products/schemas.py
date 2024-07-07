from pydantic import BaseModel


class CreateUserProduct(BaseModel):
    user_id: int
    product_id: int
