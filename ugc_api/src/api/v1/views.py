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
