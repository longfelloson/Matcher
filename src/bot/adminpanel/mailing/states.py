from aiogram.fsm.state import StatesGroup, State


class MailingState(StatesGroup):
    text = State()
