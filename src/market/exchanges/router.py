from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from database import db, SessionWithCommit, SessionWithoutCommit
from market.payments import crud as payments_crud
from market.payments.fkwallet import wallet
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
    session: AsyncSession = Depends(db.get_session_without_commit)
):
    try: 
        await payments_crud.create_payment(data, user.id, session)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"msg": "Ошибка при создании платежа"}
        )
    
    try:
        await crud.create_exchange(data, data.id, user.id, session)
    except Exception :
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"msg": "Ошибка при создании обмена"}
        )

    try: 
        await wallet.withdraw(
            data.id, data.destination, data.account, data.amount
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"msg": "Ошибка при выводе средств"}
        )
    
    return RESOURCE_CREATED_RESPONSE


@router.get("/exchanges", response_model=list[Exchange])
async def get_exchanges_endpoint(
    session: SessionWithoutCommit, params: OffsetLimit = Depends(),
):
    exchanges = await crud.get_exchanges(params.offset, params.limit, session)
    return exchanges


@router.get("/exchanges/{exchange_id}", response_model=Exchange)
async def get_exchange_endoint(
    exchange_id: UUID4, session: SessionWithoutCommit,
):
    exchange = await crud.get_exchange(exchange_id, session)
    if not exchange:
        return RESOURCE_NOT_FOUND_RESPONSE
    
    return exchange


@router.get("/exchanges/{exchange_id}")
async def delete_exchange_endpoint(
    exchange_id: UUID4, session: SessionWithCommit
):
    await crud.delete_exchange(exchange_id, session)

    return RESOURCE_DELETED_RESPONSE
