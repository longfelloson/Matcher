from fastapi import APIRouter, Depends

from database import SessionWithCommit, SessionWithoutCommit
from market.auth.utils import CurrentUser
from market.payments import crud
from market.payments.schemas import CreatePayment, Payment
from market.responses import RESOURCE_CREATED_RESPONSE
from market.schemas import OffsetLimit

router = APIRouter(tags=["Payments"])


@router.post("/payments")
async def create_payment_endpoint(
    data: CreatePayment,
    user: CurrentUser,
    session: SessionWithCommit,
):
    await crud.create_payment(data, user.id, session)
    
    return RESOURCE_CREATED_RESPONSE


@router.get("/payments", response_model=list[Payment])
async def get_payments(
    session: SessionWithoutCommit, params: OffsetLimit = Depends(),
):
    payments = await crud.get_payments(params.offset, params.limit, session)
    return payments
