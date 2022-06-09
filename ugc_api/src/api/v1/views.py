from core.decorators import login_required
from core.utils.translation import gettext_lazy as _
from fastapi import APIRouter, Depends, Request, status
from models.views import Progress, ViewProgress
from services.views import ViewService, get_view_service

router = APIRouter()


@router.get('/movie/{movie_id}/progress',
            summary='Получить прогресс просмотра фильма',
            description='Получить прогресс просмотра фильма',
            status_code=status.HTTP_202_ACCEPTED)
@login_required
async def get_progress(
    user_id: str,
    movie_id: str,
    request: Request,
    service: ViewService = Depends(get_view_service)
):
    data = {
        'user_id': user_id,  # request.user.identity
        'movie_id': movie_id,
    }
    progress = await service.get_object_or_404(ViewProgress, data)
    return progress.viewed_frame


@router.post('/movie/{movie_id}/progress',
             summary='Сохранить прогресс просмотра фильма',
             description='Отправка события о прогрессе просмотра фильма',
             status_code=status.HTTP_202_ACCEPTED)
@login_required
async def send_progress(
    user_id: str,
    movie_id: str,
    progress: Progress,
    request: Request,
    service: ViewService = Depends(get_view_service)
):
    data = {
        'user_id': user_id,  # request.user.identity
        'movie_id': movie_id,
    }
    view_progress = await service.get_object_or_none(ViewProgress, data)
    key = f"{user_id}:{movie_id}"

    if view_progress is None:
        instance = ViewProgress(viewed_frame=progress.viewed_frame, **data)
        result = await service.create(key, instance.dict(by_alias=True))
    else:
        result = await service.update(key, view_progress.dict(by_alias=True),
                                      progress.dict())

    return result
