from uuid import UUID

from core.decorators import login_required
from core.utils.translation import gettext_lazy as _
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.reviews import Review, ReviewVote, Text, Vote
from services.reviews import ReviewsService, get_reviews_service
from services.reviews_votes import (ReviewsVotesService,
                                    get_reviews_votes_service)

router = APIRouter()


@router.get('/movie/{movie_id}/reviews',
            summary='Рецензии к фильму',
            description='Просмотр рецензий к фильму',
            status_code=status.HTTP_200_OK)
async def get_movie_reviews(
    movie_id: str,
    service: ReviewsService = Depends(get_reviews_service)
):
    reviews = await service.get_reviews_by('movie_id', movie_id)
    return reviews


@router.get('/user/{user_id}/reviews',
            summary='Рецензии пользователя',
            description='Просмотр рецензий пользователя к фильмам',
            status_code=status.HTTP_200_OK)
async def get_user_reviews_of_movies(
    user_id: str,
    service: ReviewsService = Depends(get_reviews_service)
):
    reviews = await service.get_reviews_by('user_id', user_id)
    return reviews


@router.get('/review/{review_id}',
            summary='Прочитать рецензию',
            description='Прочитать рецензию к фильму',
            status_code=status.HTTP_200_OK)
async def get_review(
    review_id: str,
    request: Request,
    service: ReviewsService = Depends(get_reviews_service)
):
    review = await service.get_details(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=_('Review does not exist'),
        )
    return review


@router.post('/movie/{movie_id}/reviews',
             summary='Добавить рецензию',
             description='Добавить рецензию к фильму',
             status_code=status.HTTP_201_CREATED)
@login_required
async def add_review(
    user_id: str,
    movie_id: str,
    text: Text,
    request: Request,
    service: ReviewsService = Depends(get_reviews_service)
):
    data = {
        'user_id': user_id,  # request.user.identity
        'movie_id': movie_id
    }
    movie_review = await service.exist(data)

    if movie_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_('You already added a review to the movie'),
        )

    review = Review(text=text.text, **data)
    key = f"{user_id}:{movie_id}"
    result = await service.create(key, review.dict(by_alias=True))
    return result


@router.patch('/review/{review_id}',
              summary='Редактировать рецензию',
              description='Редактировать рецензию к фильму',
              status_code=status.HTTP_200_OK)
@login_required
async def edit_review(
    user_id: str,
    review_id: str,
    text: Text,
    request: Request,
    service: ReviewsService = Depends(get_reviews_service)
):
    review = await service.retrieve({'_id': UUID(review_id)})

    if not review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_('Review does not exist'),
        )

    review = Review(**review)

    if review.user_id != user_id:  # request.user.identity
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=_('Access denied'),
        )
    key = f"{review.user_id}:{review.movie_id}"
    result = await service.update(key, review.dict(by_alias=True), text.dict())
    return result


@router.delete('/review/{review_id}',
               summary='Удалить рецензию',
               description='Удалить рецензию к фильму',
               status_code=status.HTTP_204_NO_CONTENT)
@login_required
async def delete_review(
    user_id: str,
    review_id: str,
    request: Request,
    service: ReviewsService = Depends(get_reviews_service)
):
    review = await service.retrieve({'_id': UUID(review_id)})

    if not review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_('Review does not exist'),
        )

    review = Review(**review)

    if review.user_id != user_id:  # request.user.identity
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=_('Access denied'),
        )

    key = f"{review.user_id}:{review.movie_id}"
    await service.destroy(key, review.dict(by_alias=True))


@router.post('/review/{review_id}/vote',
             summary='Голосовать за рецензию',
             description='Добавление лайка или дизлайка к рецензии',
             status_code=status.HTTP_200_OK)
@login_required
async def vote_for_review(
    user_id: str,
    review_id: str,
    vote: Vote,
    request: Request,
    service: ReviewsVotesService = Depends(get_reviews_votes_service)
):
    data = {
        'user_id': user_id,  # request.user.identity
        'review_id': review_id
    }
    vote_review = await service.exist(data)
    key = f"{user_id}:{review_id}"

    if not vote_review:
        vote = ReviewVote(vote=vote.vote, **data)
        result = await service.create(key, vote.dict(by_alias=True))
    else:
        result = await service.update(key, data, vote.dict())

    return result
