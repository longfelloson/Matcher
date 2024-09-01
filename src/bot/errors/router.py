from aiogram import Router
from aiogram.types import ErrorEvent

from logger import logger

router = Router(name="Errors")


@router.errors()
async def errors_handler(error: ErrorEvent) -> None:
    exception_text = str(error.exception)

    if not exception_text:
        exception_text = "Возникла непредвиденная ошибка в работе бота ⚠️"

    if error.update.callback_query:
        await error.update.callback_query.message.answer(exception_text)
    else:
        await error.update.message.answer(exception_text)

    logger.error(exception_text)
