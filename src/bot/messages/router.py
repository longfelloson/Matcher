import asyncio

from aiogram import Router, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import market_link_keyboard
from bot.constants import BACK_BUTTON_EMOJI
from bot.messages.enums import ChangeProfileAnswer
from bot.texts.users import get_profile_text
from bot.users import crud as users_crud
from bot.users.enums.answers import WarningAnswer
from bot.users.enums.statuses import UserStatus
from bot.users.guesses.router import router as guesses_router
from bot.users.keyboards import (
    user_profile_keyboard,
    change_user_profile_section_keyboard,
)
from bot.users.models import User
from bot.users.rates.router import router as rates_router
from bot.users.registration.router import router as registration_router
from bot.users.states import UserChangeState
from bot.users.utils import send_user_to_react
from market.auth.token import get_auth_link

NO_PHOTO_DELAY = 2

router = Router(name="Messages")
router.include_routers(registration_router, guesses_router, rates_router)


@router.message(F.text == "Начать ▶️")
async def view_user_button_handler(
        message: Message,
        session: AsyncSession,
        state: FSMContext,
        user: User,
):
    if user.status == UserStatus.inactive:
        return await message.answer(WarningAnswer.turn_on_profile)

    await send_user_to_react(message, user, session, state)


@router.message(F.text == "Магазин 🛍")
async def market_button_handler(message: Message):
    await message.answer(
        text="Перейди по ссылке ниже, чтобы обменять баллы ⤵️",
        reply_markup=market_link_keyboard(link=get_auth_link(user_id=message.chat.id)),
    )


@router.message(F.text == "Профиль 📱")
@router.message(UserChangeState.sections, F.text == BACK_BUTTON_EMOJI)
async def profile_button_handler(
        message: Message,
        user: User,
        state: FSMContext,
):
    await state.set_state(UserChangeState.profile)

    # Задержка на случай, если фото не успелось загрузиться в S3
    if not user.photo_url:
        await asyncio.sleep(NO_PHOTO_DELAY)

    await message.answer_photo(
        photo=user.photo_url,
        caption=get_profile_text(user),
        reply_markup=user_profile_keyboard(user.config.guess_age, user.status)
    )


# @router.message(UserChangeState.profile, F.text.regexp("Угадывать возраст"))
# async def change_user_guess_age_button_handler(
#     message: Message,
#     user: User,
#     session: AsyncSession,
# ):
#     """Обработка кнопки "Угадывать возраст"""
#     new_value = False if message.text == "Угадывать возраст: ✅" else True
#     answer = Answer.user_guesses_age if new_value else Answer.user_not_guesses_age
#
#     await configs_crud.update_user_config(
#         message.chat.id, column_name="guess_age", session=session
#     )
#
#     config = await configs_crud.get_user_config(message.chat.id, session)
#     await message.answer(answer, reply_markup=user_profile_keyboard(config.guess_age, user.status))


@router.message(UserChangeState.profile, F.text == "Изменить анкету 📝")
@router.message(or_f(*UserChangeState.__all_states__[1:]), F.text == BACK_BUTTON_EMOJI)
async def change_user_profile_button_handler(message: Message, state: FSMContext):
    """Обработка кнопки "Изменить профиль"""
    await state.set_state(UserChangeState.sections)
    await message.answer(
        ChangeProfileAnswer.profile,
        reply_markup=change_user_profile_section_keyboard(),
    )


@router.message(UserChangeState.profile, F.text == "Отключить анкету 😴")
async def turn_off_user(
        message: Message,
        user: User,
        session: AsyncSession,
):
    """Отключение анкеты из системы поиска"""
    await users_crud.update_user(user.user_id, session, status=UserStatus.inactive)
    await message.answer(
        text="Твоя анкета отключена, скорее возвращайся 😇",
        reply_markup=user_profile_keyboard(user.config.guess_age, UserStatus.inactive)
    )


@router.message(UserChangeState.profile, F.text == "Включить анкету 🚀")
async def turn_on_user(
        message: Message,
        user: User,
        session: AsyncSession,
):
    """Отключение анкеты из системы поиска"""
    await users_crud.update_user(user.user_id, session, status=UserStatus.active)
    await message.answer(
        text="Твоя анкета включена, быстрее начинай оценивать 🤩",
        reply_markup=user_profile_keyboard(user.config.guess_age, UserStatus.active)
    )
