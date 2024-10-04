from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.captcha.utils import decrypt_correctness
from bot.loader import bot
from bot.users.enums.actions import UserAction
from bot.users.registration.enums.answers import SectionAnswer
from bot.users.registration.states import RegistrationState

router = Router()


@router.callback_query(F.data.startswith(UserAction.select_captcha_emoji))
async def captcha_button_handler(call: CallbackQuery, state: FSMContext):
    """Обработка решения капчи"""
    encrypted_captcha_correctness = call.data.split("*")[1]
    decrypted_captcha_correctness = decrypt_correctness(encrypted_captcha_correctness)

    if decrypted_captcha_correctness == "CORRECT":
        await bot.answer_callback_query(call.id)
        await call.message.delete()
        await state.set_state(RegistrationState.age)
        await call.message.answer(SectionAnswer.age)
    else:
        await call.answer(text="Неправильный эмодзи 🤷‍♂️", show_alert=True)
