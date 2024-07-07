from fastapi import APIRouter

from market.exchange.router import router as exchange_router
from market.products.router import router as products_router

router = APIRouter()

router.include_router(products_router)
router.include_router(exchange_router)
