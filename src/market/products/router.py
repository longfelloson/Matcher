import base64
import uuid
from fastapi import APIRouter, Depends
from pydantic import UUID4

from database import DatabaseSession
from market.products.schemas import CreateProduct, Product
from market.responses import (
    RESOURCE_CREATED_RESPONSE, 
    RESOURCE_DELETED_RESPONSE,
)
from market.products import crud
from market.schemas import OffsetLimit
from s3 import s3_client

router = APIRouter(tags=["Products"])


@router.post("/products")
async def create_product_endpoint(
    data: CreateProduct, session: DatabaseSession
):
    img_name = str(uuid.uuid4())
    img = base64.b64decode(data.img_base64)
    img_url = s3_client.get_file_url(img_name)

    await s3_client.upload_file(img_name, img)
    await crud.create_product(data, img_url, session)

    return RESOURCE_CREATED_RESPONSE


@router.get("/products", response_model=list[Product])
async def get_products_endpoint(
    session: DatabaseSession, params: OffsetLimit = Depends()
):
    products = await crud.get_products(params.offset, params.limit, session)
    return products


@router.delete("/products/{product_id}")
async def delete_product_endpoint(product_id: UUID4, session: DatabaseSession):
    await crud.delete_product(product_id, session)

    return RESOURCE_DELETED_RESPONSE
