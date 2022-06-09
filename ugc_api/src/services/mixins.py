from typing import Optional
import orjson


class RetrieveModelMixin:
    async def retrieve(self, query, projection=None):
        return await self.data_manager.get(query, projection)


class ListModelMixin:
    async def list(self, query={}, projection=None,
                   sort=None, skip=None, limit=None):
        results = await self.data_manager.all(query, projection,
                                              sort, skip, limit)
        if not results:
            return []
        return results


class CreateModelMixin:
    async def create(self, key: str, data: dict):
        result = await self.data_manager.create(key, data)
        if not result['id']:
            return None
        return result


class UpdateModelMixin:
    async def update(self, key: str, obj, data: dict):
        result = await self.data_manager.update(key, obj, data)
        if not result['modified_count']:
            return None
        return result


class DestroyModelMixin:
    async def destroy(self, key: str, data: dict):
        result = await self.data_manager.delete(key, data)
        return result


class SendMixin:
    async def send(self, data: dict) -> Optional[dict]:
        key = f"{data['user_id']}:{data['movie_id']}".encode()
        value = orjson.dumps(data)
        result = await self.broker_manager.send(self.topic, value, key)
        return result
