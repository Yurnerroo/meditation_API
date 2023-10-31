from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.base_crud import BaseCrud
from db.models.post import Post
from db.models.user import User
from db.schemas.post_schema import PostCreate, PostUpdate, PostAdminCreate


class PostCrud(BaseCrud[Post, PostCreate, PostUpdate]):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        super().__init__(model=Post, db_session=db_session)

    async def create_post(
            self,
            post_in: PostCreate,
            current_user: User,
    ) -> Post:
        db_post = Post(
            title=post_in.title,
            description=post_in.description,
            photo=post_in.photo,
            owner=current_user.id,
        )
        self.db.add(db_post)
        await self.db.flush()

        return db_post

    async def create_post_admin(
            self,
            post_in: PostAdminCreate,
            current_user: User,
    ) -> Post:
        db_post = Post(
            title=post_in.title,
            description=post_in.description,
            photo=post_in.photo,
            owner=current_user.id,
            status=post_in.status,
        )
        self.db.add(db_post)
        await self.db.flush()

        return db_post
