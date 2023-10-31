from __future__ import annotations

from datetime import datetime

from email_validator import validate_email
from pydantic import BaseModel, EmailStr, Field, validator

from db.models.user import UserTypesEnum
from utils.partial import optional


def password_size(v: str):
    assert len(v) >= 8, "must be at least 8 characters"
    assert len(v) <= 32, "must be at most 32 characters"
    return v


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=25)
    avatar: str | None = None

    @validator("name")
    def name_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v


class UserRead(UserBase):
    id: int
    user_type: str | None = None

    class Config:
        orm_mode = True


class UserReadResponse(UserRead):
    pass


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=32)


# All these fields are optional
class UserUpdate(BaseModel):
    name: str | None = None
    avatar: str | None = None
    password: str | None = None

    @validator("name")
    def name_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v

    class Config:
        orm_mode = True

    _validate_password = validator("password", allow_reuse=True)(password_size)


# All these fields are optional
@optional
class UserUpdateMe(BaseModel):
    password: str | None = None

    _validate_password = validator("password", allow_reuse=True)(password_size)


class UserFilter(BaseModel):
    name: str | None = Field(
        None, example="Username", description="Searched substring in the user name"
    )
    avatar: str | None = Field(
        None,
        example="Avatar image link",
        description="Searched substring in the avatar link",
    )
    user_type: UserTypesEnum | None = Field(
        None, example="user", description="User Type"
    )
