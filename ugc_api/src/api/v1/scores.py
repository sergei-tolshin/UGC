from core.decorators import login_required
from core.utils.translation import gettext_lazy as _
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.scores import Score, ScoreModel, ScoreResponseModel
from services.scores import ScoresService, get_scores_service

router = APIRouter()


@router.get('/{movie_id}/',
            summary='Рейтинг фильма',
            description='Просмотр средней пользовательской оценки фильма',
            response_model=ScoreResponseModel,
            status_code=status.HTTP_200_OK)
async def get_movie_score(
    movie_id: str,
    service: ScoresService = Depends(get_scores_service)
):
    result = await service.get_scores(movie_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=_('Movie does not exist'),
        )
    return result


@router.post('/{movie_id}/',
             summary='Оценка фильма пользователем',
             description='Поставить оценку фильму',
             response_model=ScoreResponseModel,
             status_code=status.HTTP_201_CREATED)
@login_required
async def rate_movie(
    movie_id: str,
    score: ScoreModel,
    request: Request,
    service: ScoresService = Depends(get_scores_service)
):
    user_id = request.user.identity
    data = {
        'user_id': user_id,
        'movie_id': movie_id,
    }
    movie_is_rated = await service.exist(data)

    key = f"{user_id}:{movie_id}"
    if movie_is_rated:
        result = await service.update(key, data, {'score': score.score})
    else:
        instance = Score(score=score.score, **data)
        result = await service.create(key, instance.dict(by_alias=True))

    return result


@router.delete('/{movie_id}/',
               summary='Удаление оценки пользователем',
               description='Удалить оценку фильма',
               response_model=ScoreResponseModel,
               status_code=status.HTTP_200_OK)
@login_required
async def delete_movie_score(
    movie_id: str,
    request: Request,
    service: ScoresService = Depends(get_scores_service)
):
    user_id = request.user.identity
    data = {
        'user_id': user_id,
        'movie_id': movie_id,
    }
    movie_is_rated = await service.exist(data)

    if not movie_is_rated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_('Movie does not have your score'),
        )
    key = f"{user_id}:{movie_id}"
    result = await service.destroy(key, data)
    return result
