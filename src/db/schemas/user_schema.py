from __future__ import annotations

from datetime import datetime

from email_validator import validate_email
from pydantic import BaseModel, EmailStr, Field, validator

from utils.partial import optional


def password_size(v: str):
    assert len(v) >= 8, "must be at least 8 characters"
    assert len(v) <= 32, "must be at most 32 characters"
    return v


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=25)
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=50)
    is_active: bool | None = False
    is_super_user: bool | None = False
    is_approved: bool | None = False
    created_by_user_id: int | None = None

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v

    @validator("email")
    def email_validator(cls, v):
        email = validate_email(v, check_deliverability=False)
        return email.normalized


class UserReadShort(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=25)
    created_by_user_id: int | None = None

    class Config:
        orm_mode = True


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserReadResponse(UserRead):
    pass


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=32)


# All these fields are optional
class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    is_active: bool | None = False
    is_approved: bool | None = False
    password: str | None = None

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v

    @validator("email")
    def email_validator(cls, v):
        email = validate_email(v, check_deliverability=False)
        return email.normalized

    class Config:
        orm_mode = True

    _validate_password = validator("password", allow_reuse=True)(password_size)


# All these fields are optional
@optional
class UserUpdateMe(BaseModel):
    password: str | None = None

    _validate_password = validator("password", allow_reuse=True)(password_size)


class UserInDB(UserRead):
    password_hash: str


class JournalistCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=25)
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=32)


class UserDetailSchema(BaseModel):
    id: int
    username: str
    full_name: str | None
    email: str | None
    is_active: bool
    is_super_user: bool
    is_approved: bool
    created_by_user_id: int | None
    created_by_user_name: str | None
    date_joined: str
    group_id: int | None
    group_name: str | None


class UserFilter(BaseModel):
    username: str | None = Field(
        None, example="User name", description="Searched substring in the user name"
    )
    full_username: str | None = Field(
        None,
        example="User full name",
        description="Searched substring in the user full name",
    )
    email: str | None = Field(
        None, example="Users email ", description="Searched substring in the user email"
    )
    group_id: int | None = Field(None, example="3", description="Group ID")
    is_approved: bool | None = Field(None, example="1", description="Is approved")
    is_active: bool | None = Field(None, example="1", description="Is active")
    created_by_user: int | None = Field(
        None, example="1", description="Created by user id"
    )
    start_date: datetime | None = Field(
        None, example="2021-01-30 01:20:00", description="Format: YYYY-MM-DD HH:MM:SS"
    )
    end_date: datetime | None = Field(
        None, example="2021-01-30 01:20:00", description="Format: YYYY-MM-DD HH:MM:SS"
    )
