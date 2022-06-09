<<<<<<< HEAD
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
=======
import uuid
import jwt

from typing import Union, Optional
from datetime import datetime
from fastapi import Header, HTTPException
from pydantic import BaseModel
from http import HTTPStatus

from services import views as views_service
from core import config
from core.initialize import router
from core.logger import log


class Stamp(BaseModel):
    user_id: Optional[uuid.UUID] = None
    movie_id: uuid.UUID
    viewed_frame: int
    duration: int
    event_time: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }

    def get_user_id(self, token):
        token = token.split(" ")
        if len(token) == 2:
            token = token[1]
        else:
            token = token[0]
        decoded_token = jwt.decode(
            token, config.JWT_SECRET, algorithms=config.JWT_ALGORITHMS
        )
        return decoded_token["user_id"]

    def set_user_id(self, token):
        self.user_id = self.get_user_id(token)


@router.post("/views/")
async def post_stamp(
    stamp: Stamp, authorization: Union[str, None] = Header(default=None)
):
    stamp.set_user_id(authorization)
    try:
        await views_service.post_stamp(stamp)
    except Exception as e:
        log.exception("views")
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR)
    return []


@router.get("/views/centry")
async def centry():
    await views_service.get_centry()
    return []
>>>>>>> 974a4387db5902ea85778809cb15d1e51072f51c
