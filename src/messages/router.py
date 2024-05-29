from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.messages.registration.utils import set_previous_state
from src.messages.schemas import Answers
from src.guesses import crud as guesses_crud
from src.text.utils import get_profile_text
from src.users.configs import crud as configs_crud
from src.users.keyboards import user_profile_keyboard, change_user_profile_section_keyboard
from src.users.models import User
from src.users.states import UserStates
from src.users.utils import send_photo

router = Router(name='Messages')


@router.message(F.text.in_({'↩️', '↩'}))
async def back_button_handler(message: Message, state: FSMContext):
    """
    Обработка кнопки "Назад" в любом из состояний регистрации
    """
    await set_previous_state(message, state)


@router.message(F.text == "Начать")
async def rate_button_handler(message: Message, session: AsyncSession, state: FSMContext, user: User):
    """
    Обработка кнопки "Старт" и выдача фото для угадывания возраста или оценки
    """
    await send_photo(message, user, session, state)


@router.message(F.text == "Профиль")
async def profile_button_handler(message: Message, user: User, session: AsyncSession, state: FSMContext) -> None:
    """
    Обработка кнопки "Профиль"
    """
    await state.set_state(UserStates.profile)

    total_points = await guesses_crud.get_total_user_guesses_points(user.user_id, session)
    caption = (
        f"Instagram:  <code>{user.instagram}</code>"
        if user.instagram
        else None
    )
    photo = await message.answer_photo(user.photo_file_id, caption)

    config = await configs_crud.get_user_config(user.user_id, session)
    await photo.reply(get_profile_text(user, total_points), reply_markup=user_profile_keyboard(config))


@router.message(UserStates.profile, F.text.regexp('Угадывать возраст'))
async def change_user_guess_age(message: Message, session: AsyncSession):
    """
    Обработка кнопки "Угадывать возраст"
    """
    new_value = False if message.text == 'Угадывать возраст: ✅' else True
    answer = Answers.USER_GUESSES_AGE if new_value else Answers.USER_NOT_GUESSES_AGE

    await configs_crud.update_user_config(message.chat.id, 'guess_age', session)

    config = await configs_crud.get_user_config(message.chat.id, session)
    await message.answer(answer, reply_markup=user_profile_keyboard(config))


@router.message(F.text == 'Изменить 📝')
async def change_user_guess_rate(message: Message, state: FSMContext):
    """
    Обработка кнопки "Изменить профиль"
    """
    await state.set_state(UserStates.change_profile)
    await message.answer(Answers.CHANGE_PROFILE, reply_markup=change_user_profile_section_keyboard())
