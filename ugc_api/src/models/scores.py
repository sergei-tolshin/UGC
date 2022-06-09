from pydantic import Field

from models.base import BaseModel, OrjsonMixin


class ScoreModel(OrjsonMixin):
    score: int = Field(default=0, gte=0, lte=10)


class Score(BaseModel, ScoreModel):
    user_id: str
    movie_id: str


class ScoreResponseModel(OrjsonMixin):
    movie_id: str = None
    rating: float = 0
    like: int = 0
    dislike: int = 0
    score_count: int = 0
