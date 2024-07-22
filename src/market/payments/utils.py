import hashlib
import hmac
import json

import aiohttp

from config import settings
from market.payments.schemas import CreatePayment

KEY = settings.PAYMENTS.KEY
KEY_ID = settings.PAYMENTS.KEY_ID
SHOP_ID = settings.PAYMENTS.SHOP_ID
MERCHANT_ID = settings.PAYMENTS.MERCHANT_ID

PAYOUT_TOKEN = f"{KEY_ID}:{KEY}"

DEFAULT_PAYMENT_METHOD = "withdraw"
DEFAULT_PAYMENT_DESCRIPTION = "Выплата средств за обмен баллов в @GuessOrRateBot"
DEFAULT_PAYMENT_COUNTRY = "Russia"


async def create_payment(create_payment_data: CreatePayment, currency: str = "RUB") -> bool:
    """

    """
    signature = create_signature(
        create_payment_data.invoice_id,
        create_payment_data.amount,
        method_id=DEFAULT_PAYMENT_METHOD,
        key_1=KEY_ID
    )
    data = {
        "shop_id": SHOP_ID,
        "invoice_id": create_payment_data.invoice_id,
        "amount": create_payment_data.amount,
        "description": DEFAULT_PAYMENT_DESCRIPTION,
        "method": DEFAULT_PAYMENT_METHOD,
        "country": DEFAULT_PAYMENT_COUNTRY,
        "currency": currency,
        "signature": signature
    }
    async with aiohttp.ClientSession() as session:
        response = await session.post(url="api.finpay.llc/payments", data=data)
        json_response = await response.json()
        return json_response['status']


def create_signature(invoice_id: str, amount: int, method_id: int, key_1: str) -> str:
    """
    Создание подписи для платежа
    """
    string = f"{MERCHANT_ID}:{invoice_id}:{amount}:{method_id}:{key_1}"
    signature = hashlib.md5(string.encode("utf-8")).hexdigest()

    return signature
