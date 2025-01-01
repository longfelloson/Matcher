from typing import Union, List

from aiogram.enums import ParseMode, ContentType
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.types import Message, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot
from bot.users import crud as users_crud
from bot.users.enums.statuses import UserStatus
from bot.users.guesses.answers import Answer
from bot.users.guesses.keyboards import rate_user_keyboard
from bot.users.models import User
from bot.users.rates import crud
from bot.users.rates.enums import RateType
from bot.users.rates.keyboards import notification_keyboard
from bot.users.rates.schemas import Rate


async def react_for_user_rate(
        message: Message,
        user: User,
        user_for_rate: User,
        session: AsyncSession,
) -> None:
    """Реакция на пользовательскую оценку с помощью кнопок"""
    rate = Rate(
        rater=user.user_id,
        rated=user_for_rate.user_id,
        rate_type=RateType.positive if message.text == "❤" else RateType.negative,
    )
    if rate.rate_type == RateType.positive:
        await send_rate_notification(
            user_id=user_for_rate.user_id,
            text="Кому-то понравилась ваша анкета 🥰",
            keyboard=notification_keyboard(rate.rater),
            session=session
        )

    await crud.add_rate(rate, session)


async def send_rate_notification(
        user_id: Union[str, int],
        text: str,
        session: AsyncSession,
        keyboard: InlineKeyboardMarkup = None,
        content_type: ContentType = ContentType.TEXT,
        photo: str = None,
) -> None:
    """Отправляет уведомление о том, что пользователь кому-то понравился"""
    try:
        if content_type == ContentType.TEXT:
            await bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
        elif content_type == ContentType.PHOTO:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
    except (TelegramForbiddenError, TelegramBadRequest):
        await users_crud.update_user(user_id, session, status=UserStatus.left)


async def get_rated_users_ids(user_id: int, session: AsyncSession) -> List[int]:
    rates = await crud.get_user_rates(user_id, session)
    return set(rate.rated for rate in rates)


async def send_user_to_rate(
        rater: User,
        rated: User,
        caption: str,
) -> Message:
    """Отправляет пользователя для его оценки"""
    photo = await bot.send_photo(
        chat_id=rater.user_id,
        caption=caption,
        photo=rated.photo_url
    )
    await photo.answer(
        text=Answer.rate_user, reply_markup=rate_user_keyboard()
    )


def was_user_rated(user_to_rate: User, rated_users_ids: List[int]) -> bool:
    return user_to_rate.user_id in rated_users_ids
