from core import config
from motor.motor_asyncio import AsyncIOMotorClient

from db.storage import AbstractStorage


class MongoDBStorage(AbstractStorage):
    def __init__(self,
                 client: AsyncIOMotorClient,
                 db_name: str = config.MONGODB_DB,
                 ):
        self.client = client
        self.db = self.client[db_name]

    async def get(self, collection, query, projection):
        collection = self.db[collection]
        document = await collection.find_one(query, projection)
        return document

    async def all(self, collection, query, projection, sort, skip, limit):
        collection = self.db[collection]
        cursor = collection.find(query, projection)
        if sort:
            cursor.sort(sort)
        if skip:
            cursor.skip(skip)
        if limit:
            cursor.limit(limit)
        return [document async for document in cursor]

    async def create(self, collection: str, document: dict):
        result = await self.db[collection].insert_one(document)
        return {'id': str(result.inserted_id)}

    async def update(self, collection: str, obj: dict, update: dict):
        collection = self.db[collection]
        result = await collection.update_many(obj, {'$set': update})
        return {
            'matched_count': result.matched_count,
            'modified_count': result.modified_count
        }

    async def delete(self, collection: str, query: dict):
        collection = self.db[collection]
        result = await collection.delete_many(query)
        return {
            'acknowledged': result.acknowledged,
            'deleted_count': result.deleted_count
        }

    async def exist(self, collection: str, document: dict) -> bool:
        count = await self.db[collection].count_documents(document)
        return count > 0

    async def count(self, collection: str, document: dict) -> bool:
        return await self.db[collection].count_documents(document)

    async def aggregate(self, collection: str, pipeline):
        collection = self.db[collection]
        result = [_ async for _ in collection.aggregate(pipeline)]
        return result

    async def close(self) -> None:
        await self.client.close()
