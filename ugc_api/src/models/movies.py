from uuid import UUID

from models.base import OrjsonMixin


class Movie(OrjsonMixin):
    id: UUID
    favorite: bool
    rating: float
    rating_count: int
    review_count: int
