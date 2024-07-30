from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from market.payments import crud, schemas
from market.payments.fkwallet import wallet

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create-payment", response_class=JSONResponse)
async def create_payment(data: schemas.CreatePayment, session: AsyncSession = Depends(get_async_session)):
    """
    Ручка для создания платежа и вывода средств на указанные реквизиты
    """
    await wallet.withdraw(**data.model_dump())

    return JSONResponse({"status": "success", "payment_id": await crud.create_payment(data, session)})
