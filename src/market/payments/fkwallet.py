import hashlib
import json
from abc import ABC, abstractmethod
from typing import Optional

import aiohttp
from pydantic import UUID4

from config import settings
from logger import logger
from market.payments.enums import PaymentDestination


SBERBANK_ID_FOR_SPB = "1enc00000111"
TINKOFF_ID_FOR_SPB = "1enc00000004"

RUB_CURRENCY_ID = 1

PAYMENT_SYSTEM_SBP_ID = 5
PAYMENT_SYSTEM_CARD_ID = 6
PAYMENT_SYSTEM_YOOMONEY_ID = 7

FEE_FROM_BALANCE = 1
FEE_FROM_PAYMENT = 0

CARD_NUMBER_SYMBOLS_AMOUNT = 16


class PaymentSystem(ABC):
    @property
    @abstractmethod
    def withdraw_endpoint_url(self) -> str:
        pass

    @abstractmethod
    async def withdraw(self, *args, **kwargs):
        pass

    @abstractmethod
    async def _request(self, *args, **kwargs):
        pass


class Wallet(PaymentSystem):
    def __init__(self, base_url: str, private_key: str, public_key: str, account: str):
        self.private_key = private_key
        self.public_key = public_key
        self.base_url = base_url
        self.account = account

    @property
    def withdraw_endpoint_url(self) -> str:
        """
        Возвращает URL эндпоинта для отправки запроса для вывода средств с кошелька
        """
        return f"{self.base_url}/{self.public_key}/withdrawal"

    @staticmethod
    def get_payment_system_id(account: str) -> int:
        if len(account.replace(" ", "")) == CARD_NUMBER_SYMBOLS_AMOUNT:
            return PAYMENT_SYSTEM_CARD_ID
        return PAYMENT_SYSTEM_SBP_ID
    
    @staticmethod
    def get_sbp_bank_id(destination: PaymentDestination) -> int:
        if destination == PaymentDestination.sberbank:
            return SBERBANK_ID_FOR_SPB
        elif destination == PaymentDestination.tbank:
            return TINKOFF_ID_FOR_SPB

    def __create_sign(self, data: Optional[dict]) -> str:
        """
        Создает подпись с помощью приватного ключа
        """
        sigh = hashlib.sha256(
            json.dumps(data).encode() + self.private_key.encode()
        ).hexdigest()
        if not data:
            sigh = hashlib.sha256(self.private_key.encode()).hexdigest()

        return sigh

    async def _request(self, url: str, method: str = "POST", data: dict = None) -> dict:
        """
        Отправляет запрос с нужными данными
        """
        sign = self.__create_sign(data)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {sign}",
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method, url, data=data, headers=headers
                ) as response:
                    return await response.json()
        except Exception as e:
            await logger.error(f"Ошибка при отправке запроса для создания платежа: {e}")

    async def withdraw(
        self,
        payment_id: UUID4,
        destination: PaymentDestination,
        account: str,
        amount: int | float,
        currency_id: int = RUB_CURRENCY_ID, 
        fee_from_balance: int = FEE_FROM_PAYMENT,
    ) -> dict:
        """
        Выводит средства с кошелька на указанные реквизиты
        """
        data = {
            "idempotence_key": payment_id,
            "currency_id": currency_id,
            "payment_system_id": self.get_payment_system_id(account),
            "fee_from_balance": fee_from_balance,
            "account": self.account,
            "amount": amount,
        }
        if data["payment_system_id"] == PAYMENT_SYSTEM_SBP_ID:
            data["fiels"] = {"sbp_bank_id": self.get_sbp_bank_id(destination)}

        return await self._request(self.withdraw_endpoint_url, data=data)


wallet = Wallet(
    base_url=settings.PAYMENTS_BASE_URL,
    private_key=settings.PAYMENTS_PRIVATE_KEY,
    public_key=settings.PAYMENTS_PUBLIC_KEY,
    account=settings.PAYMENTS_ACCOUNT,
)
