from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: int
    birthday: date
    user_id: int


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: int
    birthday: date
    user_id: int

    class Config:
        orm_mode = True


class ContactModel(ContactBase):
    pass


class ContactUpdate(ContactModel):
    pass


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=16)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
