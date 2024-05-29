from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, BotCommandScopeChatMember, BotCommandScopeAllPrivateChats, BotCommandScopeChat, \
    Message

from src import config
from src.bot.loader import bot, dp
from src.bot.middlewares import PayloadMiddleware, UserStatusMiddleware
from src.database import create_tables
from src.messages.commands.router import router as commands_router
from src.messages.registration.router import router as registration_router
from src.messages.router import router as messages_router
from src.rates.router import router as rates_router
from src.guesses.router import router as guesses_router
from src.reports.router import router as reports_router
from src.users.router import router as users_router


async def start() -> None:
    """
    Запуск бота
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
    Установка команд
    """
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="help", description="Поддержка")
        ]
    )
    for ADMIN_ID in config.ADMINS_IDS:
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
    Установка прослоек для бота
    """
    dp.update.outer_middleware(PayloadMiddleware())
    dp.message.middleware(UserStatusMiddleware())
