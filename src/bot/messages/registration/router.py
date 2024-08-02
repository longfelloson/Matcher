from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard
from bot.messages.registration.keyboards import (
    select_gender_keyboard,
    select_preferred_gender_keyboard,
    select_age_group_keyboard,
    select_location_keyboard,
    back_button_keyboard,
)
from bot.messages.registration.schemas import IncorrectDataAnswer, Answer, RegistrationSectionAnswer
from bot.messages.registration.states import RegistrationStates
from bot.messages.registration.utils import complete_user_registration
from bot.messages.utils import (
    validate_age,
    validate_user_name,
    validate_user_input,
)
from bot.users.configs.schemas import UserConfig
from bot.users.enums import (
    UserGender,
    PreferredAgeGroup,
)
from bot.users.geo.schemas import Location
from bot.users.geo.utils import reverse_geocode_user_location
from s3 import s3_client

router = Router(name="Registration")

MIN_USER_AGE = 13
MAX_USER_AGE = 29


@router.message(RegistrationStates.age)
async def user_age_state_handler(message: Message, state: FSMContext):
    """
    Обработка пользовательского возраста
    """
    if not validate_age(message.text, MIN_USER_AGE, MAX_USER_AGE):
        await message.answer(IncorrectDataAnswer.age)
    else:
        await state.update_data(age=int(message.text))
        await state.set_state(RegistrationStates.name)
        await message.answer(
            RegistrationSectionAnswer.name, reply_markup=back_button_keyboard()
        )


@router.message(RegistrationStates.name)
async def user_name_state_handler(message: Message, state: FSMContext):
    """
    Обработка пользовательского имени
    """
    if not validate_user_name(message.text):
        await message.answer(IncorrectDataAnswer.name)
        return

    await state.update_data(name=message.text)
    await state.set_state(RegistrationStates.gender)
    await message.answer(
        RegistrationSectionAnswer.gender, reply_markup=select_gender_keyboard()
    )


@router.message(RegistrationStates.gender)
async def user_gender_state_handler(message: Message, state: FSMContext):
    """
    Обработка пользовательского гендера
    """
    keyboard = select_gender_keyboard()
    if not await validate_user_input(message, keyboard):
        return

    gender = UserGender.male if message.text == "Парень" else UserGender.female

    await state.update_data(gender=gender)
    await state.set_state(RegistrationStates.preferred_gender)
    await message.answer(
        RegistrationSectionAnswer.preferred_gender,
        reply_markup=select_preferred_gender_keyboard(),
    )


@router.message(RegistrationStates.preferred_gender)
async def user_preferred_gender_state_handler(message: Message, state: FSMContext):
    """
    Обработка пользовательского гендера анкет
    """
    keyboard = select_preferred_gender_keyboard()
    if not await validate_user_input(message, keyboard):
        return

    preferred_gender = (
        UserGender.male if message.text == "Парней" else UserGender.female
    )

    await state.update_data(preferred_gender=preferred_gender)
    await state.set_state(RegistrationStates.preferred_age_group)
    await message.answer(
        RegistrationSectionAnswer.preferred_age_group, reply_markup=select_age_group_keyboard()
    )


@router.message(RegistrationStates.preferred_age_group)
async def preferred_age_group_state_handler(
        message: Message, state: FSMContext, data: dict
):
    """
    Получение выбранной возрастной группы
    """
    keyboard = select_age_group_keyboard()
    if not await validate_user_input(message, keyboard):
        return

    match message.text:
        case PreferredAgeGroup.Age.first:
            data["preferred_age_group"] = PreferredAgeGroup.first
        case PreferredAgeGroup.Age.second:
            data["preferred_age_group"] = PreferredAgeGroup.second
        case PreferredAgeGroup.Age.third:
            data["preferred_age_group"] = PreferredAgeGroup.third

    await state.update_data(preferred_age_group=data["preferred_age_group"])
    await state.set_state(RegistrationStates.location)
    await message.answer(
        RegistrationSectionAnswer.location, reply_markup=select_location_keyboard()
    )


@router.message(RegistrationStates.location)
async def location_state_handler(message: Message, state: FSMContext):
    """
    Получение локации или города пользователя
    """
    city = message.text
    location = message.location
    if location:
        city = await reverse_geocode_user_location(
            Location(**message.location.model_dump())
        )
        location = f"{location.longitude}*{location.latitude}"

    await state.update_data(location=location, city=city)
    await state.set_state(RegistrationStates.photo)
    await message.answer(RegistrationSectionAnswer.photo, reply_markup=back_button_keyboard())


@router.message(RegistrationStates.photo)
async def photo_state_handler(
        message: Message, state: FSMContext, session: AsyncSession
):
    """
    Получение фотографии пользователя и последующая загрузка в БД
    """
    if message.content_type == "photo":
        user_reg_info = await state.get_data()

        profile_photo_telegram_file_id = message.photo[-1].file_id
        user_reg_info["photo_url"] = s3_client.get_file_url(
            file_name=profile_photo_telegram_file_id
        )

        user_config_schema = UserConfig(user_id=message.chat.id, guess_age=True)

        await state.clear()
        await message.answer(Answer.completed_user_profile, reply_markup=main_keyboard())
        await complete_user_registration(
            user_config_schema,
            profile_photo_telegram_file_id,
            message,
            user_reg_info,
            session,
        )
    else:
        await message.answer(IncorrectDataAnswer.photo)
