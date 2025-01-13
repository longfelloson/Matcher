from pydantic import BaseModel
from pydantic.types import UUID4, Base64Str


class ProductBase(BaseModel):
    name: str
    price: int | float


class Product(ProductBase):
    id: UUID4
    img_url: str


class CreateProduct(ProductBase):
    img_base64: Base64Str
