from pydantic import BaseModel

class RecommendBase(BaseModel):
    storename: str
    rating: int

class RecommendCreate(RecommendBase):
    username:str 