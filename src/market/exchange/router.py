from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users import crud as users_crud
from bot.users.models import User
from config import settings
from database import get_async_session
from market.auth.utils import auth_guard, get_current_user
from market.exchange.schemas import ExchangeData
from market.transactions import crud as transactions_crud
from market.transactions.schemas import TransactionType

router = APIRouter(tags=["Exchange"], dependencies=[Depends(auth_guard)])
templates = Jinja2Templates(directory=settings.MARKET.TEMPLATES_PATH)


@router.get("/exchange", response_class=HTMLResponse)
async def exchange_page(request: Request):
    """
    Return HTML exchange page
    """
    return templates.TemplateResponse("exchange.html", {"request": request})


@router.post("/exchange-points", response_class=JSONResponse)
async def exchange_points_endpoint(
        data: ExchangeData,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user)
):
    """
    Endpoint to exchange user exchange.
    """
    await users_crud.decrease_user_points(user.user_id, data.points, session)
    await transactions_crud.create_transaction(TransactionType.PURCHASE, data.product_id, data.points, session)

    return JSONResponse({"message": "Points successfully exchanged"})


@router.get("/get-exchange-rate", response_class=JSONResponse)
async def get_exchange_rate_endpoint():
    """
    Endpoint for getting points exchange rate.
    """
    return JSONResponse({"current-rate": settings.EXCHANGE_RATE})


@router.get('/get-user-points', response_class=JSONResponse)
async def get_user_points_endpoint(user_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Returns JSON with user points amount by his ID
    """
    user_points = await users_crud.get_user_points(user_id, session)
    return JSONResponse({"user_points": user_points})
