from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    fullname: Optional[str] = None


class UserCreate(UserBase):
    password: str
    is_superuser: bool


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    fullname: Optional[str] = None
    password: Optional[str] = None
    is_superuser: Optional[bool] = None


class UserInDB(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    fullname: Optional[str] = None
    is_superuser: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
