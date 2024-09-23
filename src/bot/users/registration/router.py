from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard
from bot.users.configs.schemas import UserConfig
from bot.users.enums.answers import IncorrectInputAnswer
from bot.users.locations import reverse_geocode_user_location
from bot.users.registration.constants import COMPLETED_REGISTRATION_ANSWER
from bot.users.registration.enums.answers import SectionAnswer
from bot.users.registration.keyboards import (
    select_gender_keyboard,
    select_preferred_gender_keyboard,
    select_location_keyboard,
    back_button_keyboard,
    select_viewer_gender_keyboard,
)
from bot.users.registration.schemas import (
    UserAge,
    UserName,
    UserPreferredGender,
    UserGender,
    UserCity, UserRegistrationInfo, UserViewerGender,
)
from bot.users.registration.states import RegistrationState
from bot.users.registration.utils import complete_user_registration
from s3 import s3_client

router = Router(name="Registration")


@router.message(RegistrationState.age)
async def user_age_state_handler(message: Message, state: FSMContext):
    """Обработка пользовательского возраста"""
    try:
        age = UserAge(age=message.text)

        await state.update_data(age=age.age)
        await state.set_state(RegistrationState.name)
        await message.answer(
            SectionAnswer.name, reply_markup=back_button_keyboard()
        )

    except ValidationError:
        await message.answer(IncorrectInputAnswer.age)


@router.message(RegistrationState.name, F.content_type == ContentType.TEXT)
async def user_name_state_handler(message: Message, state: FSMContext):
    """Обработка пользовательского имени"""
    if message.text == "↩":
        await state.set_state(RegistrationState.age)
        return await message.answer(SectionAnswer.age, reply_markup=ReplyKeyboardRemove())

    try:
        name = UserName(name=message.text)

        await state.update_data(name=name.name)
        await state.set_state(RegistrationState.gender)
        await message.answer(SectionAnswer.gender, reply_markup=select_gender_keyboard())

    except ValidationError:
        await message.answer(IncorrectInputAnswer.name)


@router.message(RegistrationState.gender)
async def user_gender_state_handler(message: Message, state: FSMContext):
    """Обработка пользовательского гендера"""
    if message.text == "↩":
        await state.set_state(RegistrationState.name)
        return await message.answer(SectionAnswer.name, reply_markup=ReplyKeyboardRemove())

    try:
        gender = UserGender(input=message.text).convert_input_to_enum()

        await state.update_data(gender=gender)
        await state.set_state(RegistrationState.preferred_gender)
        await message.answer(SectionAnswer.preferred_gender, reply_markup=select_preferred_gender_keyboard())

    except ValidationError:
        await message.answer(IncorrectInputAnswer.buttons)


@router.message(RegistrationState.preferred_gender)
async def user_preferred_gender_state_handler(message: Message, state: FSMContext):
    """Обработка предпочитаемого к просмотру гендера анкет"""
    if message.text == "↩":
        await state.set_state(RegistrationState.gender)
        return await message.answer(SectionAnswer.gender, reply_markup=select_gender_keyboard())

    try:
        preferred_gender = UserPreferredGender(input=message.text).convert_input_to_enum()

        await state.update_data(preferred_gender=preferred_gender)
        await state.set_state(RegistrationState.viewer_gender)
        await message.answer(SectionAnswer.viewer_gender, reply_markup=select_viewer_gender_keyboard())

    except ValidationError:
        await message.answer(IncorrectInputAnswer.buttons)


@router.message(RegistrationState.viewer_gender)
async def viewer_gender_state_handler(message: Message, state: FSMContext):
    if message.text == "↩":
        await state.set_state(RegistrationState.preferred_gender)
        return await message.answer(SectionAnswer.preferred_gender, reply_markup=select_preferred_gender_keyboard())

    try:
        viewer_gender = UserViewerGender(input=message.text).convert_input_to_enum()

        await state.update_data(viewer_gender=viewer_gender)
        await state.set_state(RegistrationState.location)
        await message.answer(SectionAnswer.location, reply_markup=select_location_keyboard())

    except ValidationError:
        await message.answer(IncorrectInputAnswer.buttons)


@router.message(RegistrationState.location)
async def location_state_handler(message: Message, state: FSMContext):
    """Получение локации или города пользователя"""
    if message.text == "↩":
        await state.set_state(RegistrationState.viewer_gender)
        return await message.answer(SectionAnswer.viewer_gender, reply_markup=select_viewer_gender_keyboard())

    try:
        if location := message.location:
            city = await reverse_geocode_user_location(location.latitude, location.longitude)
            location_str = f"{location.longitude}*{location.latitude}"
            await state.update_data(location=location_str, city=city)
        else:
            city = UserCity(city=message.text).city
            await state.update_data(city=city)

        await state.set_state(RegistrationState.photo)
        await message.answer(SectionAnswer.photo, reply_markup=back_button_keyboard())

    except ValidationError:
        await message.answer(IncorrectInputAnswer.city)


@router.message(RegistrationState.photo)
async def photo_state_handler(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
):
    """Получение фотографии пользователя и последующая загрузка в БД"""
    if message.text == "↩":
        await state.set_state(RegistrationState.location)
        return await message.answer(SectionAnswer.location, reply_markup=select_location_keyboard())

    if message.content_type != ContentType.PHOTO:
        return await message.answer(IncorrectInputAnswer.photo)

    data = await state.get_data()
    photo_answer = await message.answer(text="Фото загружается...", reply_markup=ReplyKeyboardRemove())

    await state.clear()

    profile_photo_telegram_file_id = message.photo[-1].file_id
    photo_url = s3_client.get_file_url(file_name=profile_photo_telegram_file_id)

    user_config = UserConfig(user_id=message.chat.id, guess_age=True)
    user_registration_info = UserRegistrationInfo(**data, user_id=user_config.user_id, photo_url=photo_url)

    await complete_user_registration(user_config, profile_photo_telegram_file_id, user_registration_info, session)
    await photo_answer.delete()
    await message.answer(COMPLETED_REGISTRATION_ANSWER, reply_markup=main_keyboard())
