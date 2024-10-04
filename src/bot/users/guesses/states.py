from aiogram.fsm.state import State, StatesGroup


class GuessesState(StatesGroup):
    user_age = State()
