from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.keyboards import main_keyboard
from src.messages.registration.keyboards import select_gender_keyboard, select_preferred_gender_keyboard, \
    select_age_group_keyboard, select_location_keyboard, back_button_keyboard
from src.messages.registration.schemas import IncorrectDataAnswer, Answers
from src.messages.registration.states import RegistrationStates
from src.messages.utils import validate_age, validate_user_name, validate_user_input
from src.users import crud as users_crud
from src.users.configs import crud as configs_crud
from src.users.configs.schemas import UserConfig
from src.users.geo.schemas import Location
from src.users.geo.utils import reverse_geocode_user_location
from src.users.schemas import UserGender, PreferredAgeGroup, UserStatuses

router = Router(name="Registration")

MIN_USER_AGE = 13
MAX_USER_AGE = 29


@router.message(RegistrationStates.age)
async def user_age_state_handler(message: Message, state: FSMContext):
    """
    Обработка пользовательского возраста
    """
    if not validate_age(message.text, MIN_USER_AGE, MAX_USER_AGE):
        await message.answer(IncorrectDataAnswer.INVALID_AGE)
    else:
        await state.update_data(age=int(message.text))
        await state.set_state(RegistrationStates.name)
        await message.answer(Answers.USER_NAME_SECTION, reply_markup=back_button_keyboard())


@router.message(RegistrationStates.name)
async def user_name_state_handler(message: Message, state: FSMContext):
    """
    Обработка пользовательского имени
    """
    if not validate_user_name(message.text):
        await message.answer(IncorrectDataAnswer.INVALID_NAME)
        return

    await state.update_data(name=message.text)
    await state.set_state(RegistrationStates.gender)
    await message.answer(Answers.USER_GENDER_SECTION, reply_markup=select_gender_keyboard())


@router.message(RegistrationStates.gender)
async def user_gender_state_handler(message: Message, state: FSMContext):
    """
    Обработка пользовательского гендера
    """
    keyboard = select_gender_keyboard()
    if not await validate_user_input(message, keyboard):
        return

    gender = UserGender.MALE if message.text == "Парень" else UserGender.FEMALE

    await state.update_data(gender=gender)
    await state.set_state(RegistrationStates.preferred_gender)
    await message.answer(Answers.PREFERRED_GENDER_SECTION, reply_markup=select_preferred_gender_keyboard())


@router.message(RegistrationStates.preferred_gender)
async def user_gender_state_handler(message: Message, state: FSMContext):
    """
    Обработка пользовательского гендера анкет
    """
    keyboard = select_preferred_gender_keyboard()
    if not await validate_user_input(message, keyboard):
        return

    preferred_gender = UserGender.MALE if message.text == "Парней" else UserGender.FEMALE

    await state.update_data(preferred_gender=preferred_gender)
    await state.set_state(RegistrationStates.preferred_age_group)
    await message.answer(Answers.PREFERRED_AGE_GROUP_SECTION, reply_markup=select_age_group_keyboard())


@router.message(RegistrationStates.preferred_age_group)
async def preferred_age_group_state_handler(message: Message, state: FSMContext, data: dict):
    """
    Получение выбранной возрастной группы
    """
    keyboard = select_age_group_keyboard()
    if not await validate_user_input(message, keyboard):
        return

    match message.text:
        case PreferredAgeGroup.Age.FIRST:
            data['preferred_age_group'] = PreferredAgeGroup.FIRST
        case PreferredAgeGroup.Age.SECOND:
            data['preferred_age_group'] = PreferredAgeGroup.SECOND
        case PreferredAgeGroup.Age.THIRD:
            data['preferred_age_group'] = PreferredAgeGroup.THIRD

    await state.update_data(preferred_age_group=data['preferred_age_group'])
    await state.set_state(RegistrationStates.location)
    await message.answer(Answers.LOCATION_SECTION, reply_markup=select_location_keyboard())


@router.message(RegistrationStates.location)
async def location_state_handler(message: Message, state: FSMContext):
    """
    Получение локации или города пользователя
    """
    city = message.text
    location = message.location
    if location:
        city = await reverse_geocode_user_location(Location(**message.location.model_dump()))
        location = f"{location.longitude}*{location.latitude}"

    await state.update_data(location=location, city=city)
    await state.set_state(RegistrationStates.photo)
    await message.answer(Answers.USER_PHOTO, reply_markup=back_button_keyboard())


@router.message(RegistrationStates.photo)
async def location_state_handler(message: Message, state: FSMContext, session: AsyncSession):
    """
    Получение фотографии пользователя
    """
    if message.content_type == "photo":
        data = await state.get_data()
        data['photo_file_id'] = message.photo[-1].file_id

        config = UserConfig(user_id=message.chat.id, guess_age=True)

        await users_crud.update_user(message.chat.id, session, **data, status=UserStatuses.ACTIVE)
        await configs_crud.add_user_config(config, session)
        await state.clear()
        await message.answer(Answers.COMPLETED_USER_INFO, reply_markup=main_keyboard())
    else:
        await message.answer(IncorrectDataAnswer.INVALID_PHOTO)
