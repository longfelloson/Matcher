from fastapi import APIRouter

from market.exchange.router import router as exchange_router
from market.products.router import router as products_router
from market.payments.router import router as payment_router

router = APIRouter()

router.include_router(products_router)
router.include_router(exchange_router)
router.include_router(payment_router)
