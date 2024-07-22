from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_keyboard
from bot.messages.registration.keyboards import select_location_keyboard
from bot.messages.registration.schemas import IncorrectDataAnswer
from bot.messages.schemas import ChangeProfileAnswers
from bot.messages.utils import validate_user_name, validate_user_input
from bot.users import crud
from bot.users.configs import crud as users_configs_crud
from bot.users.keyboards import user_profile_keyboard, change_user_profile_section_keyboard
from bot.users.models import User
from bot.users.schemas import UserActions
from bot.users.states import UserStates

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
            await message.reply(ChangeProfileAnswers.CHANGE_USER_NAME)
        case "Возраст":
            await state.set_state(UserStates.change_age)
            await message.reply(ChangeProfileAnswers.CHANGE_AGE)
        case "Город":
            await state.set_state(UserStates.change_location)
            await message.reply(ChangeProfileAnswers.CHANGE_LOCATION, reply_markup=select_location_keyboard())
        case "Фото":
            await state.set_state(UserStates.change_photo)
            await message.reply(ChangeProfileAnswers.CHANGE_PHOTO)


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
    await message.reply(ChangeProfileAnswers.NAME_UPDATED)


@router.message(UserStates.change_location)
async def change_location_state_handler(message: Message, user: User, session: AsyncSession, state: FSMContext):
    """
    Обновление пользовательской локации
    """
    await crud.update_user(user.user_id, session, name=message.text)
    await state.set_state(UserStates.profile)
    await message.reply(ChangeProfileAnswers.LOCATION_UPDATED)


@router.message(UserStates.change_photo)
async def change_photo_state_handler(message: Message, session: AsyncSession, state: FSMContext):
    """
    Обновление пользовательской фотографии
    """
    photo_file_id = message.photo[-1].file_id

    await crud.update_user(message.chat.id, session, photo_file_id=photo_file_id)
    await state.clear()
    await message.answer(ChangeProfileAnswers.PHOTO_UPDATED, reply_markup=main_keyboard())
