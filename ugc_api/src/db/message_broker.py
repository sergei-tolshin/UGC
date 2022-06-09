from abc import ABC, abstractclassmethod, abstractmethod
from typing import Optional


class AbstractProducer(ABC):

    @abstractclassmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def send(
        self, topic: str, value: dict, key: str, action: str
    ) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass


producer: Optional[AbstractProducer] = None


async def get_producer() -> AbstractProducer:
    return producer
