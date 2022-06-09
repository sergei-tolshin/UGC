from functools import lru_cache
from uuid import UUID

from db.manager import DataManager, get_data_manager
from fastapi import Depends
from models.reviews import Review, ReviewDetails
from models.scores import Score

from .base import BaseService
from .mixins import (CreateModelMixin, DestroyModelMixin, ListModelMixin,
                     RetrieveModelMixin, UpdateModelMixin)
from .reviews_votes import ReviewsVotesService, get_reviews_votes_service
from .scores import ScoresService, get_scores_service


class ReviewsService(CreateModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     RetrieveModelMixin,
                     ListModelMixin,
                     BaseService):
    def __init__(self, data_manager, score_service, vote_service):
        super().__init__(data_manager)
        self.score = score_service
        self.vote = vote_service

    async def get_reviews_by(self, by, id):
        return await self.list({by: id})

    async def get_details(self, review_id):
        review = await self.get_object_or_404(Review, {'_id': UUID(review_id)})
        score = await self.score.get_object_or_none(
            Score,
            {'user_id': review.user_id, 'movie_id': review.movie_id}
        )
        score = score.score if score else None
        review_vote = await self.vote.get(review.id)

        return ReviewDetails(**review.dict(), **review_vote.dict(),
                             movie_scope=score)


async def data_manager():
    return await get_data_manager(db_name='ugc_db',
                                  collection='reviews',
                                  topic='reviews')


@ lru_cache()
def get_reviews_service(
        data_manager: DataManager = Depends(data_manager),
        score_service: ScoresService = Depends(get_scores_service),
        vote_service: ReviewsVotesService = Depends(get_reviews_votes_service)
) -> ReviewsService:
    return ReviewsService(data_manager, score_service, vote_service)
