from fastapi import APIRouter

from market.auth.router import router as auth_router
from market.points.router import router as points_router
from market.payments.router import router as payments_router
from market.products.router import router as products_router
from market.purchases.router import router as purchases_router
from market.exchanges.router import router as exchanges_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(products_router)
router.include_router(points_router)
router.include_router(payments_router)
router.include_router(purchases_router)
router.include_router(exchanges_router)
