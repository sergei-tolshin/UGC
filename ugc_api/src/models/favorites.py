from typing import List, Optional

from models.base import OrjsonMixin, BaseModel


class Favorite(BaseModel):
    user_id: Optional[str]
    movie_id: Optional[str]


class FavoriteCreateResponseModel(OrjsonMixin):
    inserted_id: str
    acknowledged: bool


class FavoriteListResponseModel(OrjsonMixin):
    movie_ids: Optional[List[str]]
