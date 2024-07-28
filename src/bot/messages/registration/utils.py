from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from bot.files import upload_user_photo_to_s3
from bot.keyboards import main_keyboard
from bot.messages.registration.keyboards import (
    select_preferred_gender_keyboard,
    select_age_group_keyboard,
    select_gender_keyboard,
    select_location_keyboard,
    back_button_keyboard
)
from bot.messages.registration.schemas import Answers as RegAnswers
from bot.messages.registration.states import RegistrationStates
from bot.messages.schemas import Answers
from bot.users import crud as users_crud
from bot.users.configs import crud as users_config_crud
from bot.users.schemas import UserStatus


async def set_previous_state(message: Message, state: FSMContext) -> None:
    """
    Установка предыдущего состояния
    """
    current_state = await state.get_state()
    match current_state:
        case RegistrationStates.name:
            await state.set_state(RegistrationStates.age)
            await message.answer(RegAnswers.USER_AGE_SECTION, reply_markup=ReplyKeyboardRemove())
        case RegistrationStates.gender:
            await state.set_state(RegistrationStates.name)
            await message.answer(RegAnswers.USER_NAME_SECTION, reply_markup=back_button_keyboard())
        case RegistrationStates.preferred_gender:
            await state.set_state(RegistrationStates.gender)
            await message.answer(RegAnswers.USER_GENDER_SECTION, reply_markup=select_gender_keyboard())
        case RegistrationStates.preferred_age_group:
            await state.set_state(RegistrationStates.preferred_gender)
            await message.answer(RegAnswers.PREFERRED_GENDER_SECTION, reply_markup=select_preferred_gender_keyboard())
        case RegistrationStates.location:
            await state.set_state(RegistrationStates.preferred_age_group)
            await message.answer(RegAnswers.PREFERRED_AGE_GROUP_SECTION, reply_markup=select_age_group_keyboard())
        case RegistrationStates.photo:
            await state.set_state(RegistrationStates.location)
            await message.answer(RegAnswers.LOCATION_SECTION, reply_markup=select_location_keyboard())
        case _:
            await state.clear()
            await message.answer(Answers.GREETING, reply_markup=main_keyboard())


async def complete_user_registration(
        user_config_schema,
        profile_photo_telegram_file_id: str,
        message: Message,
        user_reg_info: dict,
        session: AsyncSession,
) -> None:
    await upload_user_photo_to_s3(telegram_file_id=profile_photo_telegram_file_id)
    await users_crud.update_user(message.chat.id, session, **user_reg_info, status=UserStatus.ACTIVE)
    await users_config_crud.add_user_config(user_config_schema, session)
