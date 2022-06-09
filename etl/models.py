from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class ViewedFrameRecord:
    user_id: UUID
    movie_id: UUID
    viewed_frame: int
    event_time: datetime
