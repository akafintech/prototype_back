from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    content: str
    rating: int
    reviewer: str

class ReviewCreate(ReviewBase):
    store: str 

class ReviewUpdate(BaseModel):
    content: Optional[str] = None
    rating: Optional[int] = None
    reviewer: Optional[str] = None
    reply: Optional[str] = None
    is_replied: Optional[bool] = False

class ResponseReview(ReviewBase):
    id: int
    store: str
    reply: Optional[str] = None
    is_replied: Optional[bool] = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True