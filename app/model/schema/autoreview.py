from pydantic import BaseModel

class AutoReviewBase(BaseModel):
    storename: str
    rating: int

class AutoReviewCreate(AutoReviewBase):
    username:str 
    content:str 