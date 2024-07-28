from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.messages.rates import crud
from bot.messages.rates.schemas import Rate, RateType
from bot.users.models import User


async def react_for_user_rate(message: Message, user: User, state: FSMContext, session: AsyncSession) -> None:
    """
    Util method to react for user
    """
    data = await state.get_data()
    rate = Rate(
        rater=user.user_id,
        rated=data['user_for_rate'].user_id,
        rate_type=RateType.POSITIVE if message.text == '❤' else RateType.NEGATIVE
    )
    await crud.add_rate(rate, session)
