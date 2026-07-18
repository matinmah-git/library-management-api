from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    rating: int
    comment: str | None = None


class ReviewCreate(ReviewBase):
    book_id: int


class ReviewUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None


class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    book_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)