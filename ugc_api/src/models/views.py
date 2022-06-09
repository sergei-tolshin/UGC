from models.base import BaseModel, OrjsonMixin


class Progress(OrjsonMixin):
    viewed_frame: int


class ViewProgress(Progress, BaseModel):
    user_id: str
    movie_id: str
