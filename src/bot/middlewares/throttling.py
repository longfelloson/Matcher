import asyncio
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Update


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: int):
        super().__init__()
        self.rate_limit = rate_limit
        self.unlock_time = None  # Время, когда пользователь будет разблокирован

    @staticmethod
    async def get_last_user_action_time(state: FSMContext) -> Optional[datetime]:
        """Получение времени последнего действия пользователя из хранилища"""
        data = await state.get_data()
        last_user_action_time_str = data.get("last_user_action_time")
        if last_user_action_time_str:
            return datetime.fromisoformat(last_user_action_time_str)
        return None

    @staticmethod
    async def update_last_user_action_datetime(state: FSMContext) -> None:
        """Обновляет информацию о последнем действии пользователя в хранилище"""
        data = await state.get_data()
        data["last_user_action_time"] = datetime.now().isoformat()
        await state.set_data(data)

    async def is_allowed_to_make_request(self, last_user_action_time: Optional[datetime]) -> bool:
        """Проверяет, разрешено ли делать запрос на основе времени последнего действия"""
        if not last_user_action_time:
            return True

        time_difference = datetime.now() - last_user_action_time
        return time_difference.total_seconds() >= self.rate_limit

    @staticmethod
    async def send_warning(event: Update, text: str) -> None:
        """Отправка уведомления пользователю"""
        if event.message:
            await event.message.reply(text)

        if event.callback_query:
            await event.callback_query.answer(text)

    async def unblock_access_to_chat(self, event: Update, state: FSMContext) -> None:
        """Разблокировка доступа к чату"""
        while True:
            data = await state.get_data()
            unblock_datetime = datetime.fromisoformat(data.get("unblock_time"))
            if datetime.now() >= unblock_datetime:
                data["is_user_blocked"] = False
                data["unblock_time"] = None

                await state.set_data(data)
                await self.send_warning(event, text="Ты снова можешь что-то отправить 😊")
                break
            else:
                time_difference: timedelta = unblock_datetime - datetime.now()
                await asyncio.sleep(time_difference.total_seconds())

    async def block_access_to_chat(self, state: FSMContext) -> None:
        """Блокировка доступа к чату"""
        data = {
            "is_user_blocked": True,
            "unblock_time": (datetime.now() + timedelta(seconds=self.rate_limit)).isoformat()
        }
        await state.update_data(data)

    async def __call__(
        self,
        handler: Callable,
        event: TelegramObject,
        data: Dict,
    ):
        """Прослойка-ограничитель для скорости действий пользователя"""
        state: FSMContext = data.get("state")
        state_data = await state.get_data()
        blocked = state_data.get("is_user_blocked")

        last_action_time = await self.get_last_user_action_time(state)

        await self.update_last_user_action_datetime(state)

        if blocked:
            state_data["unblock_time"] = (datetime.now() + timedelta(seconds=self.rate_limit)).isoformat()
            await state.set_data(state_data)
            return

        if await self.is_allowed_to_make_request(last_action_time):
            return await handler(event, data)

        await self.block_access_to_chat(state)
        await self.send_warning(event, text=f"Слишком быстро, подождите секунду ⏳")

        await self.unblock_access_to_chat(event, state)
