from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field

from models.base import BaseModel, OrjsonMixin


class VoteEnum(str, Enum):
    like: str = 'like'
    dislike: str = 'dislike'


class Vote(OrjsonMixin):
    vote: VoteEnum


class ReviewVote(BaseModel, Vote):
    user_id: str
    review_id: str


class ReviewVoteDetails(OrjsonMixin):
    like: Optional[int] = 0
    dislike: Optional[int] = 0
    vote_count: Optional[int] = 0


class Text(OrjsonMixin):
    text: str = Field(min_length=10, max_length=2000)


class Review(Text, BaseModel):
    user_id: str
    movie_id: str
    created: datetime = Field(default_factory=datetime.now)


class ReviewDetails(ReviewVoteDetails, Review):
    movie_scope: Optional[int] = 0
