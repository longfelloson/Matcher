from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    age = State()
    name = State()
    gender = State()
    preferred_gender = State()
    preferred_age_group = State()
    location = State()
    photo = State()
