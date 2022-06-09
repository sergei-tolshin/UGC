from abc import ABC
from typing import Optional

from db.message_broker import AbstractProducer, get_producer
from db.storage import AbstractStorage, get_storage


class AbstractManager(ABC):
    pass


class DataManager(AbstractManager):
    def __init__(self,
                 producer: AbstractProducer,
                 storage: AbstractStorage,
                 **kwargs
                 ):
        self.producer = producer
        self.storage = storage
        self.topic = kwargs.get('topic')
        self.collection = kwargs.get('collection')

    async def get(self, query, projection):
        result = await self.storage.get(self.collection, query, projection)
        return result

    async def all(self, query, projection, sort, skip, limit):
        results = await self.storage.all(self.collection, query, projection,
                                         sort, skip, limit)
        return results

    async def create(self, key, data):
        result = await self.storage.create(self.collection, data)
        if self.producer is not None:
            await self.producer.send(
                self.topic, value=data, key=key, action='create')
        return result

    async def update(self, key, obj, data):
        result = await self.storage.update(self.collection, obj, data)
        obj.update(data)
        if self.producer is not None:
            await self.producer.send(
                self.topic, value=obj, key=key, action='update')
        return result

    async def delete(self, key, data):
        result = await self.storage.delete(self.collection, data)
        if self.producer is not None:
            await self.producer.send(
                self.topic, value=data, key=key, action='delete')
        return result

    async def exist(self, query) -> bool:
        return await self.storage.exist(self.collection, query)

    async def count(self, query):
        return await self.storage.count(self.collection, query)

    async def aggregate(self, pipeline):
        return await self.storage.aggregate(self.collection, pipeline)

    async def send(self,
                   topic: str,
                   value: bytes,
                   key: bytes) -> Optional[bool]:
        try:
            await self.producer.send(topic=topic, value=value, key=key)
        except Exception:
            return False
        else:
            return True


async def get_data_manager(**kwargs) -> DataManager:
    producer = await get_producer()
    storage = await get_storage(db_name=kwargs.get('db_name'))
    return DataManager(producer, storage, **kwargs)
