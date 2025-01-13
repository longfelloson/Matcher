from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from pydantic import UUID4

from database import DatabaseSession
from market.auth.utils import CurrentUser
from market.exchanges import crud
from market.exchanges.schemas import CreateExchange, Exchange
from market.responses import (
    RESOURCE_CREATED_RESPONSE, 
    RESOURCE_NOT_FOUND_RESPONSE,
    RESOURCE_DELETED_RESPONSE,
)
from config import settings
from market.schemas import OffsetLimit

templates = Jinja2Templates(directory=settings.TEMPLATES_PATH)
router = APIRouter(tags=["Exchanges"])


@router.post("/exchanges")
async def create_exchange_endpoint(
    data: CreateExchange,
    user: CurrentUser,
    session: DatabaseSession,
):
    await crud.create_exchange(data, user.id, session)

    return RESOURCE_CREATED_RESPONSE


@router.get("/exchanges", response_model=list[Exchange])
async def get_exchanges_endpoint(
    session: DatabaseSession, params: OffsetLimit = Depends(),
):
    exchanges = await crud.get_exchanges(params.offset, params.limit, session)
    return exchanges


@router.get("/exchanges/{exchange_id}", response_model=Exchange)
async def get_exchange_endoint(exchange_id: UUID4, session: DatabaseSession):
    exchange = await crud.get_exchange(exchange_id, session)
    if not exchange:
        return RESOURCE_NOT_FOUND_RESPONSE
    
    return exchange


@router.get("/exchanges/{exchange_id}")
async def delete_exchange_endpoint(
    exchange_id: UUID4, session: DatabaseSession
):
    await crud.delete_exchange(exchange_id, session)

    return RESOURCE_DELETED_RESPONSE
