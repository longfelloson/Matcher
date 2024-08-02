from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.files import upload_user_photo_to_s3
from bot.keyboards import main_keyboard
from bot.messages.enums import ChangeProfileAnswer
from bot.messages.registration.keyboards import select_location_keyboard
from bot.messages.registration.router import MIN_USER_AGE, MAX_USER_AGE
from bot.messages.registration.schemas import IncorrectDataAnswer
from bot.messages.utils import validate_user_name, validate_user_input, validate_age
from bot.users import crud
from bot.users.configs import crud as users_configs_crud
from bot.users.enums import UserAction
from bot.users.keyboards import (
    user_profile_keyboard,
    change_user_profile_section_keyboard,
)
from bot.users.models import User
from bot.users.states import UserStates
from s3 import s3_client

router = Router(name="Users")


@router.callback_query(F.data.regexp(UserAction.change_config))
async def change_config_button_handler(
        call: CallbackQuery, user: User, session: AsyncSession
):
    """
    Обработка кнопки "Изменить анкету пользователя"
    """
    user_config_table_column_name = call.data.split("*")[1]
    await users_configs_crud.update_user_config(
        user.user_id, user_config_table_column_name, session
    )

    config = await users_configs_crud.get_user_config(user.user_id, session)
    await call.message.edit_reply_markup(user_profile_keyboard(config))


@router.message(UserStates.change_profile)
async def change_profile_handler(message: Message, state: FSMContext):
    """
    Обновление пользовательского имени
    """
    keyboard = change_user_profile_section_keyboard()
    if not await validate_user_input(message, keyboard):
        return

    match message.text:
        case "Имя":
            await state.set_state(UserStates.change_name)
            await message.reply(ChangeProfileAnswer.change_name)
        case "Возраст":
            await state.set_state(UserStates.change_age)
            await message.reply(ChangeProfileAnswer.change_age)
        case "Город":
            await state.set_state(UserStates.change_location)
            await message.reply(
                ChangeProfileAnswer.change_location,
                reply_markup=select_location_keyboard(),
            )
        case "Фото":
            await state.set_state(UserStates.change_photo)
            await message.reply(ChangeProfileAnswer.change_photo)


@router.message(UserStates.change_name)
async def change_name_state_handler(
        message: Message, user: User, session: AsyncSession, state: FSMContext
):
    """
    Обновление пользовательского имени
    """
    if not validate_user_name(message.text):
        await message.reply(IncorrectDataAnswer.INVALID_NAME)
        return

    await crud.update_user(user.user_id, session, name=message.text)
    await state.set_state(UserStates.profile)
    await message.reply(ChangeProfileAnswer.name_updated, reply_markup=main_keyboard())


@router.message(UserStates.change_location)
async def change_location_state_handler(
        message: Message, user: User, session: AsyncSession, state: FSMContext
):
    """
    Обновление пользовательской локации
    """
    await crud.update_user(user.user_id, session, name=message.text)
    await state.set_state(UserStates.profile)
    await message.reply(
        ChangeProfileAnswer.location_updated, reply_markup=main_keyboard()
    )


@router.message(UserStates.change_photo)
async def change_photo_state_handler(
        message: Message, session: AsyncSession, state: FSMContext
):
    """
    Обновление пользовательской фотографии
    """
    file_name = message.photo[-1].file_id
    photo_url = s3_client.get_file_url(file_name)

    await state.clear()
    await upload_user_photo_to_s3(file_name)
    await crud.update_user(message.chat.id, session, photo_url=photo_url)
    await message.answer(
        ChangeProfileAnswer.photo_updated, reply_markup=main_keyboard()
    )


@router.message(UserStates.change_age)
async def change_age_state_handler(
        message: Message, user: User, session: AsyncSession, state: FSMContext
):
    """
    Смена возраста в профиле
    """
    if not validate_age(message.text, MIN_USER_AGE, MAX_USER_AGE):
        await message.answer(IncorrectDataAnswer.INVALID_AGE)
    else:
        await state.clear()
        await message.answer(
            ChangeProfileAnswer.age_updated, reply_markup=main_keyboard()
        )
        await crud.update_user(user.user_id, session, age=int(message.text))
