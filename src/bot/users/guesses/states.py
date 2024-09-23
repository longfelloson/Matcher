from aiogram.fsm.state import State, StatesGroup


class GuessesStates(StatesGroup):
    user_age = State()
