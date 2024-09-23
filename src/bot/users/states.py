from aiogram.fsm.state import StatesGroup, State


class UserChangeState(StatesGroup):
    profile = State()
    sections = State()
    name = State()
    location = State()
    age = State()
    photo = State()
    preferred_gender = State()
    gender = State()
    viewer_gender = State()
