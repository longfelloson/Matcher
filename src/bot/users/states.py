from aiogram.fsm.state import StatesGroup, State


class UserChangeState(StatesGroup):
    profile = State()
    sections = State()
    name = State()
    location = State()
    age = State()
    photo = State()
