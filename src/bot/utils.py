from aiogram.types import BotCommand, BotCommandScopeChat

from bot.adminpanel.router import router as admin_panel_router
from bot.captcha.router import router as captcha_router
from bot.loader import bot, dp
from bot.messages.commands.router import router as commands_router
from bot.messages.guesses.router import router as guesses_router
from bot.messages.rates.router import router as rates_router
from bot.messages.registration.router import router as registration_router
from bot.messages.router import router as messages_router
from bot.middlewares import PayloadMiddleware, BlockedUserMiddleware
from bot.reports.router import router as reports_router
from bot.users.router import router as users_router
from config import settings
from database import create_tables


async def start() -> None:
    """
    Устанавливает настройки для бота и запускает его
    """
    dp.include_routers(
        captcha_router,
        messages_router,
        registration_router,
        commands_router,
        rates_router,
        guesses_router,
        reports_router,
        users_router,
        admin_panel_router,
    )
    set_middleware(PayloadMiddleware(), update=True, message=False)
    set_middleware(BlockedUserMiddleware(), message=True, update=False)

    await create_tables()
    await set_commands()
    await dp.start_polling(bot)


async def set_commands() -> None:
    """
    Устанавливает команды в боте
    """
    default_commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="help", description="Поддержка"),
        BotCommand(command="report", description="Жалоба"),
    ]
    await bot.set_my_commands(default_commands)

    for ADMIN_ID in settings.admins_ids:
        await bot.set_my_commands(default_commands + [
            BotCommand(
                command="admin",
                description="Панель администратора",
                scope=BotCommandScopeChat(chat_id=ADMIN_ID)
            )
        ])


def set_middleware(middleware, update=True, message=True):
    """Устанавливает 'прослойки'"""
    if update:
        dp.update.outer_middleware(middleware)

    if message:
        dp.message.middleware(middleware)
