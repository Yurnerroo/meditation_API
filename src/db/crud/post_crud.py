from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.base_crud import BaseCrud
from db.models.post import Post
from db.schemas.post_schema import PostCreate, PostUpdate


class PostCrud(BaseCrud[Post, PostCreate, PostUpdate]):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        super().__init__(model=Post, db_session=db_session)

    async def create(self, post_in: PostCreate) -> Post:
        db_post = Post(
            title=post_in.title,
            description=post_in.description,
            photo=post_in.photo,
            owner=post_in.owner,
            status=post_in.status,
        )
        self.db.add(db_post)
        await self.db.flush()

        return db_post
