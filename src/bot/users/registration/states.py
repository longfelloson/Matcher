from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    age = State()
    name = State()
    gender = State()
    preferred_gender = State()
    location = State()
    photo = State()
    viewer_gender = State
