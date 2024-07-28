from market.payments.service import PaymentSystem


class CryptoBot(PaymentSystem):
    def __init__(self):
        ...

    def withdraw_endpoint_url(self) -> str:
        pass

    async def withdraw(self, *args, **kwargs):
        pass

    async def __request(self, *args, **kwargs):
        pass
