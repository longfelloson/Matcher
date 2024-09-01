from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import manage_user_keyboard
from bot.loader import bot
from bot.reports import crud
from bot.reports.schemas import Report
from bot.users import crud as users_crud
from bot.users.enums import UserStatus
from bot.users.models import User
from bot.users.utils import send_user_to_react
from config import settings


async def react_for_report(
        call: CallbackQuery, user: User, state: FSMContext, session: AsyncSession
) -> None:
    """
    Удаление сообщения на которое была отправлена жалоба и отправка сообщения жалобы модераторам на проверку
    """
    await bot.delete_messages(
        call.from_user.id, [call.message.message_id, call.message.message_id + 1]
    )
    await send_user_to_react(call.message, user, session, state)
    for user_id in settings.BOT.MODERATOR_IDS:
        await bot.forward_message(
            chat_id=user_id,
            from_chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=manage_user_keyboard(*call.data.split("*")[1:]),
        )


async def block_user(data: str, session: AsyncSession) -> None:
    """
    Блокировка пользователя и начисление баллов за корректную жалобу
    """
    reporter_user_id, reported_user_id = data.split("*")[1:]
    report = Report(reporter=reporter_user_id, reported=reported_user_id)

    await users_crud.update_user(reported_user_id, session, status=UserStatus.blocked)
    await users_crud.increase_user_points(
        reporter_user_id, settings.BOT.POINTS_FOR_BLOCKED_USER, session
    )
    await crud.add_report(report, session)
