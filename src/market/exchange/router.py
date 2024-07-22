from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users import crud as users_crud
from config import settings
from database import get_async_session
from market.points.payments.router import router as payment_router
from market.points.schemas import ExchangeData
from market.transactions import crud as transactions_crud
from market.transactions.schemas import TransactionType

router = APIRouter(tags=["Exchange"])
router.include_router(payment_router)

templates = Jinja2Templates(directory=settings.TEMPLATES_PATH + "/points")


@router.get("/exchange-points", response_class=HTMLResponse)
async def exchange_points_page(request: Request):
    """
    Return HTML page to exchange points
    """
    return templates.TemplateResponse("points-points.html", {"request": request})


@router.post("/exchange-points", response_class=JSONResponse)
async def exchange_points_endpoint(data: ExchangeData, session: AsyncSession = Depends(get_async_session)):
    """
    Endpoint to points user points.
    """
    await users_crud.decrease_user_points(data.user_id, data.points, session)
    await transactions_crud.create_transaction(TransactionType.PURCHASE, data.product_id, data.points, session)

    return JSONResponse({"message": "Points successfully exchanged"})


@router.get("/exchange-rate", response_class=JSONResponse)
async def get_exchange_points_rate_endpoint():
    """
    Endpoint for getting exchange points rate.
    """
    return JSONResponse({"current-rate": settings.EXCHANGE_RATE})


@router.get('/get-user-points', response_class=JSONResponse)
async def get_user_points_endpoint(user_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Returns JSON with user points by his ID
    """
    user_points = await users_crud.get_user_points(user_id, session)