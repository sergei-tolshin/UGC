from functools import lru_cache

from db.manager import DataManager, get_data_manager
from fastapi import Depends
from models.reviews import ReviewVoteDetails

from .base import BaseService
from .mixins import CreateModelMixin, UpdateModelMixin


class ReviewsVotesService(CreateModelMixin,
                          UpdateModelMixin,
                          BaseService):
    async def get(self, review_id):
        pipeline = [
            {
                '$match': {'review_id': str(review_id)}
            },
            {
                '$project': {
                    'review_id': 1,
                    'vote': 1,
                    'dislike': {
                        '$cond': [{'$eq': ['$vote', 'dislike']}, 1, 0]
                    },
                    'like': {
                        '$cond': [{'$eq': ['$vote', 'like']}, 1, 0]
                    },
                }
            },
            {
                '$group': {
                    '_id': '$review_id',
                    'like': {'$sum': '$like'},
                    'dislike': {'$sum': '$dislike'},
                    'vote_count': {'$sum': 1},
                }
            },
        ]
        review_vote = await self.data_manager.aggregate(pipeline)
        return ReviewVoteDetails(**review_vote[0])


async def data_manager():
    return await get_data_manager(db_name='ugc_db',
                                  collection='reviews_votes',
                                  topic='reviews_votes')


@ lru_cache()
def get_reviews_votes_service(
        data_manager: DataManager = Depends(data_manager)
) -> ReviewsVotesService:
    return ReviewsVotesService(data_manager)
