from abc import ABC, abstractmethod

from core.utils.translation import gettext_lazy as _
from db.manager import DataManager
from fastapi import HTTPException, status


class AbstractService(ABC):
    @abstractmethod
    async def exist(self, instance):
        pass

    @abstractmethod
    async def count(self, instance):
        pass


class BaseService(AbstractService):
    def __init__(self, data_manager: DataManager):
        self.data_manager: DataManager = data_manager

    async def exist(self, data):
        return await self.data_manager.exist(data)

    async def count(self, data):
        return await self.data_manager.count(data)

    async def get_object_or_none(self, model, data):
        object = await self.data_manager.get(data, None)
        if not object:
            return None
        return model(**object)

    async def get_object_or_404(self, model, data):
        object = await self.data_manager.get(data, None)
        if not object:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=_('Object does not exist'),
            )
        return model(**object)
