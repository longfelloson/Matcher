from typing import Optional

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.captcha.keyboards import captcha_keyboard
from bot.captcha.utils import decrypt_correctness, generate_captcha
from bot.filters import NotSolvedCaptchaFilter
from bot.messages.commands.router import command_start_handler
from bot.users.models import User

router = Router()


@router.message(NotSolvedCaptchaFilter())
async def captcha_handler(message: Message):
    """
    Обработка сообщений пользователей, у которых не решена каптча. В ответ присылает капчу
    """
    captcha = generate_captcha()

    await message.answer(
        text=f'Выберите эмодзи: <span class="tg-spoiler">{captcha["correct_emoji"]}</span>',
        reply_markup=captcha_keyboard(captcha["emojis"]),
    )


@router.callback_query(F.data.startswith("select_captcha"))
async def captcha_button_handler(
        call: CallbackQuery, session: AsyncSession, state: FSMContext, user: Optional[User]
):
    """
    Обработка решения капчи
    """
    encrypted_captcha_correctness = call.data.split("*")[1]
    decrypted_captcha_correctness = decrypt_correctness(encrypted_captcha_correctness)

    if decrypted_captcha_correctness == "CORRECT":
        await call.message.delete()
        await users_crud
        await command_start_handler(call.message, session, state, user)
    else:
        await call.answer("Неправильный эмодзи 🤷‍♂️", show_alert=True)
