import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import market_link_keyboard
from bot.messages.enums import ChangeProfileAnswer
from bot.messages.guesses.router import router as guesses_router
from bot.messages.rates.router import router as rates_router
from bot.messages.registration.router import router as registration_router
from bot.texts.users import get_profile_text
from bot.users import crud as users_crud
from bot.users.enums import UserStatus
from bot.users.keyboards import (
    user_profile_keyboard,
    change_user_profile_section_keyboard,
)
from bot.users.models import User
from bot.users.states import UserChangeState
from bot.users.utils import send_user_to_react
from market.auth.token import get_auth_link

router = Router(name="Messages")
router.include_routers(registration_router, guesses_router, rates_router)


@router.message(F.text == "Начать ▶️")
async def view_user_button_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    """Обработка кнопки "Старт" и выдача фото для угадывания возраста или оценки"""
    await send_user_to_react(message, user, session, state)


@router.message(F.text == "Магазин 🛍")
async def market_button_handler(message: Message):
    """Обработка кнопки "Магазин" в главном меню"""
    await message.answer(
        text="Перейди по ссылке ниже, чтобы обменять баллы ⤵️",
        reply_markup=market_link_keyboard(link=get_auth_link(user_id=message.chat.id)),
    )


@router.message(F.text == "Профиль 📱")
@router.message(UserChangeState.sections, F.text == "↩")
async def profile_button_handler(
    message: Message,
    user: User,
    state: FSMContext,
) -> None:
    """Обработка кнопки 'Профиль'"""
    await state.set_state(UserChangeState.profile)

    # Задержка на случай, если фото не успелось загрузиться в S3
    if not user.photo_url:
        await asyncio.sleep(2)

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
@router.message(UserChangeState.name, F.text == "↩")
@router.message(UserChangeState.age, F.text == "↩")
@router.message(UserChangeState.location, F.text == "↩")
@router.message(UserChangeState.photo, F.text == "↩")
@router.message(UserChangeState.gender, F.text == "↩")
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
    await users_crud.update_user(user.user_id, session, status=UserStatus.not_active)
    await message.answer(
        text="Твоя анкета отключена, скорее возвращайся 😇",
        reply_markup=user_profile_keyboard(user.config.guess_age, UserStatus.not_active)
    )


@router.message(UserChangeState.profile, F.text == "Включить анкету 🚀")
async def turn_off_user(
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
