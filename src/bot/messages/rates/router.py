from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot
from bot.messages.guesses.keyboards import USER_RATE_BUTTONS
from bot.messages.rates.enums import RateType
from bot.messages.rates.keyboards import respond_to_rate_keyboard
from bot.messages.rates.utils import react_for_user_rate, send_notification
from bot.texts.users import get_user_link
from bot.users import crud as users_crud
from bot.users.models import User
from bot.users.utils import send_user_to_react, send_user_to_view

router = Router(name="Rates")


@router.message(F.text.in_(USER_RATE_BUTTONS))
async def rate_user_button_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    """Обработка кнопок оценки и угадывания возрасты анкеты"""
    await react_for_user_rate(message, user, state, session)
    await send_user_to_react(message, user, session, state)


@router.callback_query(F.data.startswith("view_rater_user"))
async def show_user_who_rated(call: CallbackQuery, session: AsyncSession):
    """Просмотр пользователя, который оценил анкету"""
    rater_id = int(call.data.split("*")[1])
    rater = await users_crud.get_user(rater_id, session)

    await bot.answer_callback_query(call.id)
    await call.message.delete()
    await send_user_to_view(
        photo=rater.photo_url,
        caption="Оцени пользователя, который оценил тебя ⤴️",
        keyboard=respond_to_rate_keyboard(rater),
        message=call.message,
    )


@router.callback_query(F.data.startswith("rate_user"))
async def rate_respond_button_handler(call: CallbackQuery, session: AsyncSession, user: User):
    """Оценка пользователя в ответ"""
    rate_type, rated_id = call.data.split("*")[1:]
    rated = await users_crud.get_user(int(rated_id), session)

    await bot.answer_callback_query(call.id)

    if rate_type == RateType.positive:
        rated_link = get_user_link(rated, text="пользователь")
        rater_link = get_user_link(user)

        await call.message.edit_caption(
            caption=f"Ссылка на лайкнутого пользователя: {rated_link} 💞", parse_mode="HTML"
        )
        await send_notification(rated, text=f'{rater_link} взаимно оценил Вас, общайтесь 💞')
    else:
        await call.message.delete()
