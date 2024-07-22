from aiogram.types import BotCommand, BotCommandScopeChat

from bot.app.loader import bot, dp
from bot.app.middlewares import PayloadMiddleware, UserStatusMiddleware
from bot.guesses.router import router as guesses_router
from bot.messages.commands.router import router as commands_router
from bot.messages.registration.router import router as registration_router
from bot.messages.router import router as messages_router
from bot.rates.router import router as rates_router
from bot.reports.router import router as reports_router
from bot.users.router import router as users_router
from config import settings
from database import create_tables


async def start() -> None:
    """
    Starts the bot and set necessary utils
    """
    dp.include_routers(
        messages_router, registration_router,
        commands_router, rates_router,
        guesses_router, reports_router,
        users_router
    )
    set_middlewares()

    await create_tables()
    await set_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def set_commands() -> None:
    """
    Sets up the commands
    """
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="help", description="Поддержка")
        ]
    )
    for ADMIN_ID in settings.BOT.ADMINS_IDS:
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Запуск бота"),
                BotCommand(command="help", description="Поддержка"),
                BotCommand(command="admin", description="Панель администратора")
            ],
            scope=BotCommandScopeChat(chat_id=ADMIN_ID)
        )


def set_middlewares() -> None:
    """
    Sets up the middlewares
    """
    dp.update.outer_middleware(PayloadMiddleware())
    dp.message.middleware(UserStatusMiddleware())
