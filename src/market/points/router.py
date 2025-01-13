from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bot.users import crud as users_crud
from config import settings
from database import DatabaseSession
from market.auth.utils import CurrentUser
from market.points.schemas import UpdateUserPoints
from market.points.enums import PointsOperationType
from market.responses import RESOURCE_UPDATED_RESPONSE

router = APIRouter(tags=["Points"])
templates = Jinja2Templates(settings.TEMPLATES_PATH)


@router.get("/points")
async def get_user_points(user: CurrentUser):
    return {"points": user.points}


@router.get("/points/exchange")
async def get_exchange_points_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "exchange.html")


@router.patch("/points")
async def update_user_points(
    data: UpdateUserPoints,
    user: CurrentUser,
    session: DatabaseSession,
):
    if data.operation == PointsOperationType.INCREASE:
        await users_crud.increase_user_points(user.id, data.amount, session)
    elif data.operation == PointsOperationType.DECREASE:
        await users_crud.decrease_user_points(user.id, data.amount, session)

    return RESOURCE_UPDATED_RESPONSE
