from typing import Union, List

from aiogram.enums import ParseMode, ContentType
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.types import Message, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot
from bot.users import crud as users_crud
from bot.users.enums.statuses import UserStatus
from bot.users.guesses.answers import Answer
from bot.users.models import User
from bot.users.rates.answers import RateAnswer
from bot.users.rates.keyboards import rate_buttons_keyboard
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
    rate = Rate(
        rater_user_id=user.id,
        rated_user_id=user_for_rate.id,
        type=RateType.positive if message.text == "❤" else RateType.negative,
    )
    if rate.type == RateType.positive:
        await send_rate_notification(
            user_id=user_for_rate.id,
            text=RateAnswer.someone_liked_you,
            keyboard=notification_keyboard(rate.rater_user_id),
            session=session,
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


async def send_user_to_rate(
    rater: User,
    rated: User,
    caption: str,
) -> Message:
    photo = await bot.send_photo(
        chat_id=rater.id, caption=caption, photo=rated.photo_url
    )
    await photo.answer(text=Answer.rate_user, reply_markup=rate_buttons_keyboard())


def was_user_rated(user_to_rate: User, rated_users_ids: List[int]) -> bool:
    return user_to_rate.id in rated_users_ids
