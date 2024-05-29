from typing import List

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup

from src.bot.keyboards import main_keyboard
from src.guesses.states import GuessesStates
from src.messages.registration.keyboards import select_preferred_gender_keyboard, select_age_group_keyboard, \
    select_gender_keyboard, select_location_keyboard, back_button_keyboard
from src.messages.registration.schemas import Answers as RegAnswers
from src.messages.schemas import Answers
from src.messages.registration.states import RegistrationStates


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
