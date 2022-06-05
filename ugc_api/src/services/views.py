import uuid

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from core.initialize import produce
from core.logger import log


class Stamp(BaseModel):
    user_id: Optional[uuid.UUID] = None
    movie_id: uuid.UUID
    viewed_frame: int
    duration: int
    event_time: datetime


async def post_stamp(stamp):
    value_json = stamp.json().encode("utf-8")
    await produce(value_json)
    return value_json


async def get_centry():
    try:
        division_by_zero = 1 / 0
    except Exception:
        log.exception("services.views")
        division_by_zero = 0
    return division_by_zero
