from pydantic import BaseModel, Field

from db.models.post import PostStatusesEnum
from db.schemas.user_schema import UserRead


class PostBase(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    photo: str | None = None
    description: str | None = None


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    owner: UserRead

    class Config:
        orm_mode = True


class PostReadResponse(PostRead):
    pass


# Schemas for Admin
class PostAdminBase(PostBase):
    status: PostStatusesEnum | None = None


class PostAdminCreate(PostAdminBase):
    pass


class PostAdminUpdate(PostAdminBase):
    pass
