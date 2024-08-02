from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.messages.rates import crud
from bot.messages.rates.enums import RateType
from bot.messages.rates.schemas import Rate
from bot.users.models import User


async def react_for_user_rate(
        message: Message, user: User, state: FSMContext, session: AsyncSession
) -> None:
    """
    Реакция на пользовательскую оценку с помощью кнопок
    """
    data = await state.get_data()
    rate = Rate(
        rater=user.user_id,
        rated=data["user_for_rate"].user_id,
        rate_type=RateType.positive if message.text == "❤" else RateType.negative,
    )
    await crud.add_rate(rate, session)
