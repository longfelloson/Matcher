from fastapi import (
    Depends,
    Request,
    APIRouter,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from market.auth.token import decode_token, create_access_token
from config import settings

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(settings.TEMPLATES_PATH)


@router.get("/auth")
async def get_auth_page(payload: dict = Depends(decode_token)):
    new_access_token = create_access_token(payload)

    response = RedirectResponse(url="/")
    response.set_cookie(key="token", value=new_access_token)

    return response


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
