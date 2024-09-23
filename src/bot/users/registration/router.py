from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard
from bot.messages.registration.enums.answers import RegistrationSectionAnswer
from bot.messages.registration.keyboards import (
    select_gender_keyboard,
    select_preferred_gender_keyboard,
    select_age_group_keyboard,
    select_location_keyboard,
    back_button_keyboard,
)
from bot.messages.registration.schemas import (
    UserAge,
    UserName,
    UserPreferredGender,
    UserGender,
    UserPreferredAgeGroup,
    UserCity, UserRegistrationInfo, UserViewerGender,
)
from bot.messages.registration.states import RegistrationState
from bot.messages.registration.utils import complete_user_registration
from bot.users.configs.schemas import UserConfig
from bot.users.geo.utils import reverse_geocode_user_location
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
            RegistrationSectionAnswer.name, reply_markup=back_button_keyboard()
        )
    except ValidationError:
        await message.answer("Твой возраст должен быть от 14 до 28")


@router.message(RegistrationState.name)
@router.message(RegistrationState.gender, F.text == "↩")
async def user_name_state_handler(message: Message, state: FSMContext):
    """Обработка пользовательского имени"""
    try:
        name = UserName(name=message.text)

        await state.update_data(name=name.name)
        await state.set_state(RegistrationState.gender)
        await message.answer(
            RegistrationSectionAnswer.gender, reply_markup=select_gender_keyboard()
        )
    except ValidationError:
        await message.answer("Это не похоже на имя 🤔")


@router.message(RegistrationState.gender)
@router.message(RegistrationState.preferred_gender, F.text == "↩")
async def user_gender_state_handler(message: Message, state: FSMContext):
    """Обработка пользовательского гендера"""
    try:
        gender = UserGender(input=message.text).convert_input_to_enum()

        await state.update_data(gender=gender)
        await state.set_state(RegistrationState.preferred_gender)
        await message.answer(
            RegistrationSectionAnswer.preferred_gender, reply_markup=select_preferred_gender_keyboard(),
        )
    except ValidationError:
        await message.answer("Используй кнопки 😘")


@router.message(RegistrationState.preferred_gender)
async def user_preferred_gender_state_handler(message: Message, state: FSMContext):
    """Обработка предпочитаемого к просмотру гендера анкет"""
    try:
        preferred_gender = UserPreferredGender(input=message.text).convert_input_to_enum()

        await state.update_data(preferred_gender=preferred_gender)
        await state.set_state(RegistrationState.viewer_gender)
        await message.answer(RegistrationSectionAnswer.viewer_gender, reply_markup=select_age_group_keyboard())
    except ValidationError:
        await message.answer("Используй кнопки 😘")


@router.message(RegistrationState.viewer_gender)
async def viewer_gender_state_handler(message: Message, state: FSMContext):
    try:
        viewer_gender = UserViewerGender(input=message.text).convert_input_to_enum()

        await state.update_data(viewer_gender=viewer_gender)
        await state.set_state(RegistrationState.location)
        await message.answer(RegistrationSectionAnswer.location, reply_markup=select_location_keyboard())
    except ValidationError:
        await message.answer("Используй кнопки 😘")


@router.message(RegistrationState.location)
async def location_state_handler(message: Message, state: FSMContext):
    """Получение локации или города пользователя"""
    try:
        city = UserCity(city=message.text)
        location = message.location

        if location:
            city = await reverse_geocode_user_location(location.latitude, location.longitude)
            location = f"{location.longitude}*{location.latitude}"

        await state.update_data(location=location, city=city.city)
        await state.set_state(RegistrationState.photo)
        await message.answer(RegistrationSectionAnswer.photo, reply_markup=back_button_keyboard())
    except ValidationError:
        await message.answer("Используй кнопки 😘")


@router.message(RegistrationState.photo)
async def photo_state_handler(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    """Получение фотографии пользователя и последующая загрузка в БД"""
    if message.content_type != ContentType.PHOTO:
        return await message.answer("Отправь фото 😘")
        data = await state.get_data()

        profile_photo_telegram_file_id = message.photo[-1].file_id
        photo_url = s3_client.get_file_url(file_name=profile_photo_telegram_file_id)

        user_registration_info = UserRegistrationInfo(**data, photo_url=photo_url)
        user_config = UserConfig(user_id=message.chat.id, guess_age=True)

        await state.clear()
        await complete_user_registration(
            user_config, profile_photo_telegram_file_id, user_registration_info, session
        )
        await message.answer("Твоя анкета сохранена ✅", reply_markup=main_keyboard())
    else:

