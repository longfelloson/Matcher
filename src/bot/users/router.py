from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.files import upload_user_photo_to_s3
from bot.keyboards import main_keyboard
from bot.messages.enums import ChangeProfileAnswer, UpdatedProfileAnswer
from bot.users.enums.answers import IncorrectInputAnswer
from bot.users.enums.sections import UserProfileSection
from bot.users.locations import reverse_geocode_user_location
from bot.users.registration.keyboards import select_location_keyboard, back_button_keyboard, select_gender_keyboard, \
    select_preferred_gender_keyboard, select_viewer_gender_keyboard
from bot.users.registration.schemas import UserAge, UserName, UserCity, UserGender, UserPreferredGender, \
    UserViewerGender
from bot.users import crud
from bot.users.models import User
from bot.users.states import UserChangeState
from s3 import s3_client

router = Router(name="Users")


@router.message(UserChangeState.sections)
async def change_profile_handler(message: Message, state: FSMContext):
    """Обработка кнопок выбора секции"""
    section_actions = {
        UserProfileSection.name: (
            UserChangeState.name, ChangeProfileAnswer.name, back_button_keyboard()
        ),
        UserProfileSection.age: (
            UserChangeState.age, ChangeProfileAnswer.age, back_button_keyboard()
        ),
        UserProfileSection.city: (
            UserChangeState.location, ChangeProfileAnswer.location, select_location_keyboard()
        ),
        UserProfileSection.gender: (
            UserChangeState.gender, ChangeProfileAnswer.gender, select_gender_keyboard()
        ),
        UserProfileSection.preferred_gender: (
            UserChangeState.preferred_gender, ChangeProfileAnswer.preferred_gender, select_preferred_gender_keyboard()
        ),
        UserProfileSection.photo: (
            UserChangeState.photo, ChangeProfileAnswer.photo, back_button_keyboard()
        ),
        UserProfileSection.viewer_gender: (
            UserChangeState.viewer_gender, ChangeProfileAnswer.viewer_gender, select_viewer_gender_keyboard()
        )
    }

    action = section_actions.get(message.text)

    if action:
        await state.set_state(action[0])
        await message.answer(action[1], reply_markup=action[2])
    else:
        await message.answer("Используй кнопки 😘")


@router.message(UserChangeState.name)
async def change_name_state_handler(
    message: Message,
    user: User,
    session: AsyncSession,
    state: FSMContext,
):
    """Обновление пользовательского имени"""
    try:
        name = UserName(name=message.text)

        await state.clear()
        await message.answer(UpdatedProfileAnswer.name, reply_markup=main_keyboard())
        await crud.update_user(user.user_id, session, name=name.name)
    except ValidationError:
        await message.answer("Это не похоже на имя 🤔")


@router.message(UserChangeState.location)
async def change_location_state_handler(
    message: Message,
    user: User,
    session: AsyncSession,
    state: FSMContext,
):
    """Обновление пользовательской локации"""
    try:
        city = UserCity(city=message.text).city
        location = message.location

        if location:
            city = await reverse_geocode_user_location(location.latitude, location.longitude)
            location = f"{location.longitude}*{location.latitude}"

        await state.clear()
        await message.answer(UpdatedProfileAnswer.location, reply_markup=main_keyboard())
        await crud.update_user(user.user_id, session, city=city, location=location)
    except ValidationError:
        await message.answer("Отправь город или локацию с помощью кнопки 😘")


@router.message(UserChangeState.photo)
async def change_photo_state_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
):
    """Обновление пользовательской фотографии"""
    if message.content_type != ContentType.PHOTO:
        return await message.answer(IncorrectInputAnswer.photo)

    await state.clear()

    photo_answer = await message.answer(text="Фото загружается...", reply_markup=ReplyKeyboardRemove())

    file_name = message.photo[-1].file_id
    photo_url = s3_client.get_file_url(file_name)

    await upload_user_photo_to_s3(file_name)
    await photo_answer.delete()
    await message.answer(UpdatedProfileAnswer.photo, reply_markup=main_keyboard())
    await crud.update_user(message.chat.id, session, photo_url=photo_url)


@router.message(UserChangeState.age)
async def change_age_state_handler(
    message: Message,
    user: User,
    session: AsyncSession,
    state: FSMContext,
):
    """Смена возраста в профиле"""
    try:
        age = UserAge(age=message.text)

        await state.clear()
        await message.answer(UpdatedProfileAnswer.age, reply_markup=main_keyboard())
        await crud.update_user(user.user_id, session, age=age.age)

    except ValidationError:
        await message.answer(IncorrectInputAnswer.age)


@router.message(UserChangeState.gender)
async def change_gender_state_handler(
    message: Message,
    user: User,
    state: FSMContext,
    session: AsyncSession
):
    """Смена гендера в профиле"""
    try:
        gender = UserGender(input=message.text).convert_input_to_enum()

        await state.clear()
        await message.answer(UpdatedProfileAnswer.gender, reply_markup=main_keyboard())
        await crud.update_user(user.user_id, session, gender=gender)

    except ValidationError:
        await message.answer(IncorrectInputAnswer.buttons)


@router.message(UserChangeState.preferred_gender)
async def change_preferred_gender_state_handler(
    message: Message,
    user: User,
    state: FSMContext,
    session: AsyncSession
):
    """Смена гендера анкет для просмотра"""
    try:
        preferred_gender = UserPreferredGender(input=message.text).convert_input_to_enum()

        await state.clear()
        await message.answer(UpdatedProfileAnswer.preferred_gender, reply_markup=main_keyboard())
        await crud.update_user(user.user_id, session, preferred_gender=preferred_gender)

    except ValidationError:
        await message.answer(IncorrectInputAnswer.buttons)


@router.message(UserChangeState.viewer_gender)
async def change_viewer_gender(
    message: Message,
    user: User,
    state: FSMContext,
    session: AsyncSession
):
    """Смена гендера в профиле"""
    try:
        viewer_gender = UserViewerGender(input=message.text).convert_input_to_enum()

        await state.clear()
        await message.answer(UpdatedProfileAnswer.viewer_gender, reply_markup=main_keyboard())
        await crud.update_user(user.user_id, session, viewer_gender=viewer_gender)

    except ValidationError:
        await message.answer(IncorrectInputAnswer.buttons)