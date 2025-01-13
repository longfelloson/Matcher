from aiogram import Router
from aiogram.types import ErrorEvent

from logger import logger

router = Router()


@router.error()
async def error_handler(error: ErrorEvent):
    message = (
        error.update.message
        if getattr(error.update, "message")
        else error.update.callback_query
    )

    await logger.error(f"Возникла ошибка: {error.exception}", exc_info=True)
    await message.answer("Возникла ошибка, попробуйте позже 🫨")
