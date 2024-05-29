from aiogram.fsm.state import State, StatesGroup


class GuessesStates(StatesGroup):
    guess_user_age = State()
