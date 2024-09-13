from aiogram.fsm.state import State, StatesGroup


class RateState(StatesGroup):
    user = State()
