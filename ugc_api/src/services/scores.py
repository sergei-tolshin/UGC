from functools import lru_cache

from db.manager import DataManager, get_data_manager
from fastapi import Depends

from .base import BaseService
from .mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin


class ScoresService(CreateModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    BaseService):

    async def create(self, key: str, data: dict):
        await super().create(key, data)
        result = await self.get_scores(data['movie_id'])
        return result

    async def update(self, key: str, obj: dict, update: dict):
        await super().update(key, obj, update)
        result = await self.get_scores(obj['movie_id'])
        return result

    async def destroy(self, key: str, data: dict):
        await super().destroy(key, data)
        result = await self.get_scores(data['movie_id'])
        return result

    async def get_scores(self, movie_id):
        pipeline = [
            {
                '$match': {'movie_id': movie_id}
            },
            {
                '$project': {
                    'score': 1,
                    'score0': {'$cond': [{'$eq': ['$score', 0]}, 1, 0]},
                    'score10': {'$cond': [{'$eq': ['$score', 10]}, 1, 0]},
                }
            },
            {
                '$group': {
                    '_id': movie_id,
                    'rating_avg': {'$avg': '$score'},
                    'like': {'$sum': '$score10'},
                    'dislike': {'$sum': '$score0'},
                    'score_count': {'$sum': 1},
                }
            },
            {
                '$project': {
                    'movie_id': '$_id',
                    'rating': {'$round': ["$rating_avg", 1]},
                    'like': 1,
                    'dislike': 1,
                    'score_count': 1,
                }
            },
        ]
        result = await self.data_manager.aggregate(pipeline)

        if not result:
            return None
        return result[0]


async def data_manager():
    return await get_data_manager(db_name='ugc_db',
                                  collection='scores',
                                  topic='scores')


@lru_cache()
def get_scores_service(
        data_manager: DataManager = Depends(data_manager),
) -> ScoresService:
    return ScoresService(data_manager)
