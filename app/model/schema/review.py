from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    content: str
    rating: int
    picture: Optional[str] = None

class ReviewCreate(ReviewBase):
    store_id: int 