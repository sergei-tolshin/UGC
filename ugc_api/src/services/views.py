from functools import lru_cache

from db.manager import DataManager, get_data_manager
from fastapi import Depends

from .base import BaseService
from .mixins import CreateModelMixin, UpdateModelMixin


class ViewService(CreateModelMixin,
                  UpdateModelMixin,
                  BaseService):
    pass


async def data_manager():
    return await get_data_manager(db_name='ugc_db',
                                  collection='views',
                                  topic='views')


@ lru_cache()
def get_view_service(
        data_manager: DataManager = Depends(data_manager)
) -> ViewService:
    return ViewService(data_manager)
