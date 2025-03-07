from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.captcha.enum import CaptchaCorrectness
from bot.captcha.utils import decrypt_correctness
from bot.loader import bot
from bot.users.enums.actions import UserAction
from bot.users.registration.enums.answers import SectionAnswer
from bot.users.registration.states import RegistrationState
from bot.users.registration.utils import send_warning_about_username

router = Router()


@router.callback_query(F.data.startswith(UserAction.select_captcha_emoji))
async def captcha_click_handler(call: CallbackQuery, state: FSMContext):
    encrypted_captcha_correctness = call.data.split("*")[1]
    decrypted_captcha_correctness = decrypt_correctness(encrypted_captcha_correctness)

    if decrypted_captcha_correctness == CaptchaCorrectness.CORRECT:
        await bot.answer_callback_query(call.id)
        await call.message.delete()
        await state.set_state(RegistrationState.age)
        
        # Warning about not setted username
        if not call.from_user.username:
            media_group = await send_warning_about_username(call.message)
            await media_group[0].reply(SectionAnswer.age)
        else:
            await call.message.answer(SectionAnswer.age)
    else:
        await call.answer(text="Неправильный эмодзи 🤷‍♂️", show_alert=True)
