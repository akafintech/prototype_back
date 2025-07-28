from pydantic import BaseModel, EmailStr

class StoreBase(BaseModel):
    name: str
    owner_id: int

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int

    class Config:
        orm_mode = True