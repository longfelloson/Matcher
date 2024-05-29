from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.messages.registration.keyboards import select_location_keyboard
from src.messages.registration.schemas import IncorrectDataAnswer
from src.messages.router import profile_button_handler
from src.messages.schemas import Answers
from src.messages.utils import validate_user_name, validate_user_input
from src.users import crud
from src.users.configs import crud as users_configs_crud
from src.users.keyboards import user_profile_keyboard, change_user_profile_section_keyboard
from src.users.models import User
from src.users.schemas import UserActions
from src.users.states import UserStates

router = Router(name="Users")


@router.callback_query(F.data.regexp(UserActions.CHANGE_CONFIG))
async def change_config_button_handler(call: CallbackQuery, user: User, session: AsyncSession):
    """
    Обработка кнопки "Изменить анкету пользователя"
    """
    await users_configs_crud.update_user_config(user.user_id, call.data.split('*')[1], session)

    config = await users_configs_crud.get_user_config(user.user_id, session)
    await call.message.edit_reply_markup(user_profile_keyboard(config))


@router.message(UserStates.change_profile)
async def name_profile_section(message: Message, state: FSMContext):
    """
    Обновление пользовательского имени
    """
    keyboard = change_user_profile_section_keyboard()
    if not await validate_user_input(message, keyboard):
        return

    match message.text:
        case "Имя":
            await state.set_state(UserStates.change_name)
            await message.reply(Answers.CHANGE_USER_NAME)
        case "Возраст":
            await state.set_state(UserStates.change_age)
            await message.reply(Answers.CHANGE_AGE)
        case "Город":
            await state.set_state(UserStates.change_location)
            await message.reply(Answers.CHANGE_LOCATION, reply_markup=select_location_keyboard())


@router.message(UserStates.change_name)
async def change_name_state_handler(message: Message, user: User, session: AsyncSession, state: FSMContext):
    """
    Обновление пользовательского имени
    """
    if not validate_user_name(message.text):
        await message.reply(IncorrectDataAnswer.INVALID_NAME)
        return

    await crud.update_user(user.user_id, session, name=message.text)
    await state.set_state(UserStates.profile)
    await message.reply(Answers.NAME_UPDATED)


@router.message(UserStates.change_location)
async def change_location_state_handler(message: Message, user: User, session: AsyncSession, state: FSMContext):
    """
    Обновление пользовательской локации
    """
    if not validate_user_name(message.text):
        await message.reply(IncorrectDataAnswer.INVALID_NAME)
        return

    await crud.update_user(user.user_id, session, name=message.text)
    await state.set_state(UserStates.profile)
    await message.reply(Answers.LOCATION_UPDATED)





