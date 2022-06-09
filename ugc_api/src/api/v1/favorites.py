from core.decorators import login_required
from core.utils.translation import gettext_lazy as _
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.favorites import Favorite
from services.favorites import FavoritesService, get_favorite_service

router = APIRouter()


@router.get('/favorites/',
            summary='Список избранных фильмов',
            description='Просмотр списка избранных фильмов',
            status_code=status.HTTP_200_OK)
@login_required
async def list_favorites(
    user_id: str,
    request: Request,
    service: FavoritesService = Depends(get_favorite_service)
):
    fields = {
        '_id': False,
        'movie_id': True
    }
    favorites = await service.list({'user_id': user_id}, fields)
    return [_['movie_id'] for _ in favorites]


@router.post('/movie/{movie_id}/favorites',
             summary='Добавить в избранное',
             description='Добавление фильма в избранное',
             status_code=status.HTTP_201_CREATED)
@login_required
async def favorite_movies(
    user_id: str,
    movie_id: str,
    request: Request,
    service: FavoritesService = Depends(get_favorite_service)
):
    data = {
        'user_id': user_id,  # request.user.identity
        'movie_id': movie_id
    }

    movie_in_favorites = await service.exist(data)

    if movie_in_favorites:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_('You already added this movie to favorites'),
        )

    favorite = Favorite(**data)
    key = f"{favorite.user_id}:{favorite.movie_id}"
    return await service.create(key, favorite.dict(by_alias=True))


@router.delete('/movie/{movie_id}/favorites',
               summary='Удалить из избранного',
               description='Удалить фильм из избранного',
               status_code=status.HTTP_204_NO_CONTENT)
@login_required
async def delete_movie_from_favorites(
    user_id: str,
    movie_id: str,
    request: Request,
    service: FavoritesService = Depends(get_favorite_service)
):
    data = {
        'user_id': user_id,  # request.user.identity
        'movie_id': movie_id
    }
    movie_in_favorites = await service.exist(data)

    if not movie_in_favorites:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_('You do not have this movie in favorites'),
        )
    key = f"{user_id}:{movie_id}"
    await service.destroy(key, data)
