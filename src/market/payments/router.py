from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from market.payments import (
    crud,
    schemas,
)

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create-payment", response_class=JSONResponse)
async def create_payment(data: schemas.CreatePayment, session: AsyncSession = Depends(get_async_session)):
    """
    Creates payment
    """
    ...

    return JSONResponse({"status": "success", "payment_id": await crud.create_payment(data, session)})
