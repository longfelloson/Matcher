from aiogram import Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.files import upload_user_photo_to_s3
from bot.keyboards import main_keyboard
from bot.messages.enums import ChangeProfileAnswer, UpdatedProfileAnswer
from bot.users import crud
from bot.users.enums.answers import IncorrectInputAnswer, WarningAnswer
from bot.users.enums.sections import UserProfileSection
from bot.users.locations import get_city_by_location
from bot.users.models import User
from bot.users.registration.keyboards import (
    select_location_keyboard,
    back_button_keyboard,
    select_gender_keyboard,
    select_name_keyboard,
    select_preferred_gender_keyboard,
    select_viewer_gender_keyboard,
)
from bot.users.registration.schemas import (
    UserAge,
    UserName,
    UserCity,
    UserGender,
    UserPreferredGender,
    UserViewerGender,
)
from bot.users.states import UpdateUserState
from s3 import s3_client

router = Router(name="Users")


@router.message(UpdateUserState.sections)
async def change_profile_handler(message: Message, state: FSMContext):
    """Обработка кнопок выбора секции"""
    section_actions = {
        UserProfileSection.name: (
            UpdateUserState.name,
            ChangeProfileAnswer.name,
            select_name_keyboard(message.from_user.first_name),
        ),
        UserProfileSection.age: (
            UpdateUserState.age,
            ChangeProfileAnswer.age,
            back_button_keyboard(),
        ),
        UserProfileSection.city: (
            UpdateUserState.location,
            ChangeProfileAnswer.location,
            select_location_keyboard(),
        ),
        UserProfileSection.gender: (
            UpdateUserState.gender,
            ChangeProfileAnswer.gender,
            select_gender_keyboard(),
        ),
        UserProfileSection.preferred_gender: (
            UpdateUserState.preferred_gender,
            ChangeProfileAnswer.preferred_gender,
            select_preferred_gender_keyboard(),
        ),
        UserProfileSection.photo: (
            UpdateUserState.photo,
            ChangeProfileAnswer.photo,
            back_button_keyboard(),
        ),
        UserProfileSection.viewer_gender: (
            UpdateUserState.viewer_gender,
            ChangeProfileAnswer.viewer_gender,
            select_viewer_gender_keyboard(),
        ),
    }

    action = section_actions.get(message.text)

    if action:
        state_, answer, keyboard = action

        await state.set_state(state_)
        await message.answer(answer, reply_markup=keyboard)
    else:
        await message.answer(IncorrectInputAnswer.buttons)


@router.message(UpdateUserState.name)
async def update_user_name(
    message: Message,
    user: User,
    session: AsyncSession,
    state: FSMContext,
):
    try:
        name = UserName(name=message.text)

        await state.clear()
        await message.answer(UpdatedProfileAnswer.name, reply_markup=main_keyboard())
        await crud.update_user(user.id, session, name=name.name)
    except ValidationError:
        await message.answer(IncorrectInputAnswer.name)


@router.message(UpdateUserState.location)
async def update_user_location(
    message: Message,
    user: User,
    session: AsyncSession,
    state: FSMContext,
):
    try:
        city = UserCity(city=message.text).city
        location = message.location

        if location:
            city = await get_city_by_location(location.latitude, location.longitude)
            location = f"{location.longitude}*{location.latitude}"

        await state.clear()
        await message.answer(
            UpdatedProfileAnswer.location, reply_markup=main_keyboard()
        )
        await crud.update_user(user.id, session, city=city, location=location)
    except ValidationError:
        await message.answer(IncorrectInputAnswer.city)


@router.message(UpdateUserState.photo)
async def update_user_photo(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
):
    if message.content_type != ContentType.PHOTO:
        return await message.answer(IncorrectInputAnswer.photo)

    await state.clear()

    answer_for_user_photo = await message.answer(
        WarningAnswer.photo_is_uploading, reply_markup=ReplyKeyboardRemove()
    )

    file_name = message.photo[-1].file_id
    photo_url = s3_client.get_file_url(file_name)

    await upload_user_photo_to_s3(file_name)
    await answer_for_user_photo.delete()
    await message.answer(UpdatedProfileAnswer.photo, reply_markup=main_keyboard())
    await crud.update_user(message.chat.id, session, photo_url=photo_url)


@router.message(UpdateUserState.age)
async def update_user_age(
    message: Message,
    user: User,
    session: AsyncSession,
    state: FSMContext,
):
    try:
        age = UserAge(age=message.text)

        await state.clear()
        await message.answer(UpdatedProfileAnswer.age, reply_markup=main_keyboard())
        await crud.update_user(user.id, session, age=age.age)
    except ValidationError:
        await message.answer(IncorrectInputAnswer.age)


@router.message(UpdateUserState.gender)
async def update_user_gender(
    message: Message,
    user: User,
    state: FSMContext,
    session: AsyncSession,
):
    try:
        gender = UserGender(input=message.text).convert_input_to_enum()

        await state.clear()
        await message.answer(UpdatedProfileAnswer.gender, reply_markup=main_keyboard())
        await crud.update_user(user.id, session, gender=gender)
    except ValidationError:
        await message.answer(IncorrectInputAnswer.buttons)


@router.message(UpdateUserState.preferred_gender)
async def update_user_preferred_gender(
    message: Message,
    user: User,
    state: FSMContext,
    session: AsyncSession,
):
    try:
        preferred_gender = UserPreferredGender(
            input=message.text
        ).convert_input_to_enum()
        answer = UpdatedProfileAnswer.get_preffered_gender_answer(preferred_gender)

        await state.clear()
        await message.answer(answer, reply_markup=main_keyboard())
        await crud.update_user(user.id, session, preferred_gender=preferred_gender)
    except ValidationError:
        await message.answer(IncorrectInputAnswer.buttons)


@router.message(UpdateUserState.viewer_gender)
async def update_user_viewer_gender(
    message: Message,
    user: User,
    state: FSMContext,
    session: AsyncSession,
):
    try:
        viewer_gender = UserViewerGender(input=message.text).convert_input_to_enum()
        answer = UpdatedProfileAnswer.get_viewer_gender_answer(viewer_gender)

        await state.clear()
        await message.answer(answer, reply_markup=main_keyboard())
        await crud.update_user(user.id, session, viewer_gender=viewer_gender)
    except ValidationError:
        await message.answer(IncorrectInputAnswer.buttons)
