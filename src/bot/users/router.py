from aiogram import Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.files import upload_user_photo_to_s3
from bot.keyboards import main_keyboard
from bot.messages.enums import ChangeProfileAnswer, UpdatedProfileAnswer
from bot.messages.registration.keyboards import select_location_keyboard, back_button_keyboard, select_gender_keyboard, \
    select_preferred_gender_keyboard
from bot.messages.registration.schemas import UserAge, UserName, UserCity, UserGender, UserPreferredGender
from bot.users import crud
from bot.users.enums import UserProfileSection
from bot.users.geo.utils import reverse_geocode_user_location
from bot.users.models import User
from bot.users.states import UserChangeState
from s3 import s3_client

router = Router(name="Users")


@router.message(UserChangeState.sections)
async def change_profile_handler(message: Message, state: FSMContext):
    """Обновление пользовательского имени"""
    match message.text:
        case UserProfileSection.name:
            await state.set_state(UserChangeState.name)
            await message.answer(ChangeProfileAnswer.name, reply_markup=back_button_keyboard())
        case UserProfileSection.age:
            await state.set_state(UserChangeState.age)
            await message.answer(ChangeProfileAnswer.age, reply_markup=back_button_keyboard())
        case UserProfileSection.city:
            await state.set_state(UserChangeState.location)
            await message.answer(
                ChangeProfileAnswer.location,
                reply_markup=select_location_keyboard(),
            )
        case UserProfileSection.gender:
            await state.set_state(UserChangeState.gender)
            await message.answer(
                ChangeProfileAnswer.gender,
                reply_markup=select_gender_keyboard(),
            )
        case UserProfileSection.preferred_gender:
            await state.set_state(UserChangeState.preferred_gender)
            await message.answer(
                ChangeProfileAnswer.preferred_gender,
                reply_markup=select_preferred_gender_keyboard(),
            )
        case UserProfileSection.photo:
            await state.set_state(UserChangeState.photo)
            await message.answer(ChangeProfileAnswer.photo, reply_markup=back_button_keyboard())
        case _:
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
    # TODO: улучшить момент изменения фото
    if message.content_type == ContentType.PHOTO:
        file_name = message.photo[-1].file_id
        photo_url = s3_client.get_file_url(file_name)

        await state.clear()
        await message.answer(UpdatedProfileAnswer.photo, reply_markup=main_keyboard())
        await upload_user_photo_to_s3(file_name)
        await crud.update_user(message.chat.id, session, photo_url=photo_url)
    else:
        await message.answer("Отправь фото, а не текст 😘")


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
        await message.answer("Твой возраст должен быть от 14 до 28")


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
        await message.answer("Используй кнопки 😘")


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
        await message.answer("Используй кнопки 😘")
