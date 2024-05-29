from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src import config
from src.bot.keyboards import manage_user_keyboard
from src.bot.loader import bot
from src.reports import crud
from src.reports.schemas import Report
from src.users.models import User
from src.users.schemas import UserStatuses
from src.users import crud as users_crud
from src.users.utils import send_photo


async def react_for_report(call: CallbackQuery, user: User, state: FSMContext, session: AsyncSession) -> None:
    """
    Удаление сообщения на которое была отправлена жалоба и отправка сообщения жалобы модераторам на проверку
    """
    await bot.delete_messages(call.from_user.id, [call.message.message_id, call.message.message_id + 1])
    await send_photo(call.message, user, session, state)
    for user_id in config.MODERATOR_IDS:
        await bot.forward_message(
            chat_id=user_id, from_chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=manage_user_keyboard(*call.data.split("*")[1:])
        )


async def block_user(data: str, session: AsyncSession) -> None:
    """
    Блокировка пользователя и начисление баллов за корректную жалобу
    """
    report = Report(reporter=data.split('*')[1], reported=data.split('*')[2])

    await users_crud.update_user(data.split('*')[2], session, status=UserStatuses.BLOCKED)
    await users_crud.increase_user_points(data.split('*')[1], config.POINTS_FOR_BLOCKED_USER, session)
    await crud.add_report(report, session)
