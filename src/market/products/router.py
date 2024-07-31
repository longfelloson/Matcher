from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from config import settings
from database import get_async_session
from market.auth.utils import auth_guard
from market.products import crud
from market.products.schemas import CreateUserProduct

router = APIRouter(
    tags=["Products"], prefix="/products", dependencies=[Depends(auth_guard)]
)
templates = Jinja2Templates(directory=settings.MARKET.TEMPLATES_PATH + "/products")


@router.get("/get-products", status_code=status.HTTP_200_OK)
async def get_products(
    offset: int = 0,
    limit: int = 100,
    user_id: int = None,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Ручка для получения товаров
    """
    return await crud.get_products(offset, limit, user_id, session)


@router.get("/get-product")
async def get_product_endpoint(
    product_id: int,
    session: AsyncSession = Depends(get_async_session),
    user_id: int = None,
):
    """
    Ручка для получения товара по его ID
    """
    return await crud.get_product(product_id, session, user_id)


@router.get("/product/{product_id}", response_class=HTMLResponse)
async def get_product_page(request: Request):
    """
    Ручка для получения страницы товара
    """
    return templates.TemplateResponse("product.html", {"request": request})


@router.get("/buy-product", response_class=HTMLResponse)
async def buy_product_page(request: Request):
    """
    Ручка для получения страницы покупки товара за баллы
    """
    return templates.TemplateResponse("buy-product.html", {"request": request})


@router.post("/add-user-product", response_class=JSONResponse)
async def buy_product_endpoint(
    data: CreateUserProduct, session: AsyncSession = Depends(get_async_session)
):
    """
    Ручка для добавления пользовательского товара полученного за баллы
    """
    await crud.create_user_product(data.user_id, data.product_id, session)

    return JSONResponse(
        {"message": "User product successfully created"}, status.HTTP_201_CREATED
    )
