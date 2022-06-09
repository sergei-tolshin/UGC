from abc import ABC, abstractmethod
from typing import Optional


class AbstractStorage(ABC):
    @abstractmethod
    def get(self, index, id):
        pass

    @abstractmethod
    def all(self, index, id):
        pass

    @abstractmethod
    async def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def exist(self):
        pass

    @abstractmethod
    def count(self):
        pass

    @abstractmethod
    def aggregate(self):
        pass

    @abstractmethod
    def close(self):
        pass


db: Optional[AbstractStorage] = None


async def get_storage(db_name) -> AbstractStorage:
    db.db_name = db_name
    return db
