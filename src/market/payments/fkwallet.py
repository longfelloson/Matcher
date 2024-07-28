import hashlib
import json
import uuid
from typing import Optional

import aiohttp

from config import settings
from logger import logger
from market.payments.service import PaymentSystem

SBERBANK_ID_FOR_SPB = "1enc00000111"
YOOMONEY_ID_FOR_SPB = "1enc00000022"
TINKOFF_ID_FOR_SPB = "1enc00000004"

RUB_CURRENCY_ID = 1

PAYMENT_SYSTEM_SBP_ID = 5
PAYMENT_SYSTEM_CARD_ID = 6
PAYMENT_SYSTEM_YOOMONEY_ID = 7

FEE_FROM_BALANCE = 1
FEE_FROM_PAYMENT = 0


class Wallet(PaymentSystem):
    def __init__(
            self,
            base_url: str,
            private_key: str,
            public_key: str,
            account: str
    ):
        self.private_key = private_key
        self.public_key = public_key
        self.base_url = base_url
        self.account = account

    @property
    def withdraw_endpoint_url(self) -> str:
        """
        Returns url to make request to withdraw money from wallet
        """
        return f"{self.base_url}/{self.public_key}/withdrawal"

    @staticmethod
    def __idempotence_key() -> str:
        """

        """
        return str(uuid.uuid4())

    def __create_sign(self, data: Optional[dict]) -> str:
        """
        Create a signature using the private key
        """
        sigh = hashlib.sha256(json.dumps(data).encode() + self.private_key.encode()).hexdigest()
        if not data:
            sigh = hashlib.sha256(self.private_key.encode()).hexdigest()

        return sigh

    async def __request(self, url: str, method: str = "POST", data: dict = None) -> dict:
        """
        Make a GET request to the wallet API
        """
        sign = self.__create_sign(data)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {sign}',
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, data=data, headers=headers) as response:
                    print(response.status)
                    return await response.json()
        except Exception as e:
            logger.error("Error request via payment system: %m", e)

    async def withdraw(
            self,
            sbp_bank_id: int,
            amount: float,
            payment_system_id: int,
            fee_from_balance: int = FEE_FROM_PAYMENT,
            currency_id: int = RUB_CURRENCY_ID,
    ) -> dict:
        """
        Withdraw an amount from wallet to card
        """
        data = {
            "sbp_bank_id": sbp_bank_id,
            "currency_id": currency_id,
            "payment_system_id": payment_system_id,
            "fee_from_balance": fee_from_balance,
            "account": self.account,
        }
        return await self.__request(self.withdraw_endpoint_url, data=data)


wallet = Wallet(
    base_url=settings.PAYMENTS.PAYMENTS_BASE_URL,
    private_key=settings.PAYMENTS.PAYMENTS_PRIVATE_KEY,
    public_key=settings.PAYMENTS.PAYMENTS_PUBLIC_KEY,
    account=settings.PAYMENTS.PAYMENTS_ACCOUNT,
)
