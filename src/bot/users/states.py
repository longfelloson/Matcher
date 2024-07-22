from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    profile = State()
    change_name = State()
    change_location = State()
    change_age = State()
    change_profile = State()
    change_photo = State()
