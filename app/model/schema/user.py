from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    phone_number: Optional[str] = None
    referral_code: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    new_password: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    id:int

class User(UserBase):
    id: int
    phone_number: Optional[str] = None
    referral_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 