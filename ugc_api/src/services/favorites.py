from functools import lru_cache

from db.manager import DataManager, get_data_manager
from fastapi import Depends

from .base import BaseService
from .mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin


class FavoritesService(CreateModelMixin,
                       DestroyModelMixin,
                       ListModelMixin,
                       BaseService):
    pass


async def data_manager():
    return await get_data_manager(db_name='ugc_db',
                                  collection='favorites',
                                  topic='favorites')


@lru_cache()
def get_favorite_service(
        data_manager: DataManager = Depends(data_manager),
) -> FavoritesService:
    return FavoritesService(data_manager)
