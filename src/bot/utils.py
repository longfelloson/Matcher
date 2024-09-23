from aiogram.types import BotCommand, BotCommandScopeChat

from bot.adminpanel.router import router as admin_panel_router
from bot.captcha.router import router as captcha_router
from bot.errors.router import router as errors_router
from bot.loader import bot, dp
from bot.messages.commands.router import router as commands_router
from bot.messages.router import router as messages_router
from bot.middlewares.payload import PayloadMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.middlewares.user import BlockedUserMiddleware
from bot.reports.router import router as reports_router
from bot.users.router import router as users_router
from config import settings
from database import create_tables

DEFAULT_RATE_LIMIT = 0.5


async def start() -> None:
    """Устанавливает настройки для бота и запускает его"""
    dp.include_routers(
        # errors_router,
        captcha_router,
        messages_router,
        commands_router,
        reports_router,
        users_router,
        admin_panel_router,
    )
    set_middleware(ThrottlingMiddleware(rate_limit=DEFAULT_RATE_LIMIT), for_updates=True)
    set_middleware(PayloadMiddleware(), for_updates=True)
    set_middleware(BlockedUserMiddleware(), for_messages=True)

    await create_tables()
    await set_commands()
    await dp.start_polling(bot)


async def set_commands() -> None:
    """Устанавливает команды в боте"""
    default_commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="help", description="Поддержка"),
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


def set_middleware(middleware, for_updates=False, for_messages=False):
    """Устанавливает 'прослойки'"""
    if for_updates:
        dp.update.outer_middleware(middleware)

    if for_messages:
        dp.message.middleware(middleware)
