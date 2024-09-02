from fastapi import (
    APIRouter,
    Depends,
    Request,
    status,
)
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users import crud as users_crud
from bot.users.models import User
from config import settings
from database import get_async_session
from market.auth.utils import auth_guard, get_current_user
from market.exchange.schemas import ExchangePoints
from market.transactions import crud as transactions_crud
from market.transactions.enums import TransactionType

router = APIRouter(tags=["Exchange"], dependencies=[Depends(auth_guard)])
templates = Jinja2Templates(directory=settings.TEMPLATES_PATH)


@router.get("/exchange", response_class=HTMLResponse)
async def exchange_page(request: Request):
    """Возвращает страницу для обмена баллов"""
    return templates.TemplateResponse("exchange.html", {"request": request})


@router.post("/exchange", response_class=JSONResponse, status_code=status.HTTP_201_CREATED)
async def exchange_points_endpoint(
    data: ExchangePoints,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    """Ручка для обмена баллов пользователя"""
    await users_crud.decrease_user_points(user.user_id, data.points, session)
    await transactions_crud.create_transaction(TransactionType.purchase, data.product_id, data.points, session)

    return JSONResponse({"message": "Points successfully exchanged"})


@router.get("/exchange/rate", response_class=JSONResponse)
async def get_exchange_rate():
    """Ручка получения текущего курса обмена баллов на рубли"""
    return JSONResponse({"current-rate": settings.MARKET_EXCHANGE_RATE})


@router.get("/exchange/user-points", response_class=JSONResponse)
async def get_user_points(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    """Ручка для получения баллов пользователя"""
    user_points = await users_crud.get_user_points(user.user_id, session)
    return JSONResponse({"user_points": user_points})
