from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from bot.files import upload_user_photo_to_s3
from bot.keyboards import main_keyboard
from bot.messages.commands.enums import CommandAnswer
from bot.messages.registration.keyboards import (
    select_preferred_gender_keyboard,
    select_age_group_keyboard,
    select_gender_keyboard,
    select_location_keyboard,
    back_button_keyboard,
)
from bot.messages.registration.schemas import RegistrationSectionAnswer
from bot.messages.registration.states import RegistrationStates
from bot.users import crud as users_crud
from bot.users.configs import crud as users_config_crud
from bot.users.configs.schemas import UserConfig
from bot.users.enums import UserStatus


async def set_previous_state(message: Message, state: FSMContext) -> None:
    """
    Установка предыдущего состояния
    """
    current_state = await state.get_state()
    match current_state:
        case RegistrationStates.name:
            await state.set_state(RegistrationStates.age)
            await message.answer(
                RegistrationSectionAnswer.age, reply_markup=ReplyKeyboardRemove()
            )
        case RegistrationStates.gender:
            await state.set_state(RegistrationStates.name)
            await message.answer(
                RegistrationSectionAnswer.name, reply_markup=back_button_keyboard()
            )
        case RegistrationStates.preferred_gender:
            await state.set_state(RegistrationStates.gender)
            await message.answer(
                RegistrationSectionAnswer.gender, reply_markup=select_gender_keyboard()
            )
        case RegistrationStates.preferred_age_group:
            await state.set_state(RegistrationStates.preferred_gender)
            await message.answer(
                RegistrationSectionAnswer.preferred_gender,
                reply_markup=select_preferred_gender_keyboard(),
            )
        case RegistrationStates.location:
            await state.set_state(RegistrationStates.preferred_age_group)
            await message.answer(
                RegistrationSectionAnswer.preferred_age_group,
                reply_markup=select_age_group_keyboard(),
            )
        case RegistrationStates.photo:
            await state.set_state(RegistrationStates.location)
            await message.answer(
                RegistrationSectionAnswer.location, reply_markup=select_location_keyboard()
            )
        case _:
            await state.clear()
            await message.answer(CommandAnswer.start, reply_markup=main_keyboard())


async def complete_user_registration(
    user_config_schema: UserConfig,
    profile_photo_telegram_file_id: str,
    message: Message,
    user_reg_info: dict,
    session: AsyncSession,
) -> None:
    await upload_user_photo_to_s3(telegram_file_id=profile_photo_telegram_file_id)
    await users_crud.update_user(
        message.chat.id, session, **user_reg_info, status=UserStatus.active
    )
    await users_config_crud.add_user_config(user_config_schema, session)
