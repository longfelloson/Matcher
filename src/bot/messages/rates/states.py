from aiogram.fsm.state import State, StatesGroup


class RatesStates(StatesGroup):
    rate_user = State()
