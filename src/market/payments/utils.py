import hashlib
import hmac
import json

import httpx

from config import settings
from market.exchange.payments.schemas import CreatePayment


async def send_money(data: CreatePayment) -> None:
    """

    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Signature": get_signature({"data": data})
    }
    params = {
        "amount": data.amount,
        "signature": get_signature(data),
        "shopId": settings.PAYMENTS.SHOP_ID,
        "service": data.destination,
        "subtract": 0
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.lava.ru/business/payoff/create", headers=headers, params=params)
        return response.json()


def get_signature(data: dict) -> str:
    json_str = json.dumps(data).encode()
    signature = hmac.new(bytes(settings.PAYMENTS.SECRET_KEY, 'UTF-8'), json_str, hashlib.sha256).hexdigest()
    return signature
