from typing import List
from fastapi import APIRouter, Depends
from pydantic import UUID4

from database import DatabaseSession
from market.auth.utils import CurrentUser
from market.purchases import crud
from market.purchases.schemas import CreatePurchase, Purchase
from market.responses import RESOURCE_CREATED_RESPONSE, RESOURCE_NOT_FOUND_RESPONSE
from market.schemas import OffsetLimit


router = APIRouter(tags=["Purchases"])


@router.post("/purchases")
async def create_purchase_endpoint(
    data: CreatePurchase,
    user: CurrentUser,
    session: DatabaseSession,
):
    await crud.create_purchase(data, user.id, session)

    return RESOURCE_CREATED_RESPONSE


@router.get("/purchases", response_model=List[Purchase])
async def get_purchases_endpoint(
    session: DatabaseSession, params: OffsetLimit = Depends()
):
    purchases = await crud.get_purchases(params.offset, params.limit, session)
    return purchases


@router.get("/purchases/{purchase_id}", response_model=Purchase)
async def get_purchase_endpoint(purchase_id: UUID4, session: DatabaseSession):
    purchase = await crud.get_purchase(purchase_id, session)
    if not purchase:
        return RESOURCE_NOT_FOUND_RESPONSE

    return purchase
