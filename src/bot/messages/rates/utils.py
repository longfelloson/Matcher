from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot
from bot.messages.rates import crud
from bot.messages.rates.enums import RateType
from bot.messages.rates.keyboards import notification_keyboard
from bot.messages.rates.schemas import Rate
from bot.users import crud as users_crud
from bot.users.enums import UserStatus
from bot.users.models import User


async def react_for_user_rate(
    message: Message,
    user: User,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Реакция на пользовательскую оценку с помощью кнопок"""
    data = await state.get_data()
    rate = Rate(
        rater=user.user_id,
        rated=data["user_for_rate"].user_id,
        rate_type=RateType.positive if message.text == "❤" else RateType.negative,
    )
    if rate.rate_type == RateType.positive:
        await send_notification(
            rated=data["user_for_rate"],
            text="Кому-то понравилась ваша анкета 🥰",
            keyboard=notification_keyboard(rate.rater),
            session=session
        )

    await crud.add_rate(rate, session)


async def send_notification(
        rated: User,
        text: str,
        session: AsyncSession,
        keyboard=None,
) -> None:
    """Отправляет уведомление о том, что пользователь кому-то понравился"""
    try:
        await bot.send_message(
            chat_id=rated.user_id,
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )
    except (TelegramForbiddenError, TelegramBadRequest):
        await users_crud.update_user(rated.user_id, session, status=UserStatus.left)
