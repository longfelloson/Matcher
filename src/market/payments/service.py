from abc import ABC, abstractmethod


class PaymentSystem(ABC):
    @property
    @abstractmethod
    def withdraw_endpoint_url(self) -> str:
        pass

    @abstractmethod
    async def withdraw(self, *args, **kwargs):
        pass

    @abstractmethod
    async def __request(self, *args, **kwargs):
        pass
