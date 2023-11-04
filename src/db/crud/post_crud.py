from typing import Any

from sqlalchemy import Select, select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from db.crud.base_crud import BaseCrud
from db.models.post import Post
from db.models.user import User
from db.schemas.post_schema import PostCreate, PostUpdate, PostAdminCreate, PostFilter, PostReadResponse
from db.schemas.user_schema import UserRead
from schemas.common_schema import IOrderEnum


class PostCrud(BaseCrud[Post, PostCreate, PostUpdate]):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        super().__init__(model=Post, db_session=db_session)

    async def get_post(self, post_id: int) -> PostReadResponse | None:
        owner = aliased(User, name="owner")
        query = (
            select(self.model, owner)
            .join(owner, owner.id == self.model.owner)  # type: ignore
            .where(self.model.id == post_id)
        )
        result = (await self.db.execute(query)).one_or_none()
        return PostReadResponse(
            id=result[0].id,
            title=result[0].title,
            photo=result[0].photo,
            description=result[0].description,
            owner=UserRead(
                id=result[1].id,
                name=result[1].name,
                avatar=result[1].avatar,
                user_type=result[1].user_type,
            )
        ) if result else None

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

    async def get_all_posts_ordered(
        self,
        posts_filter: PostFilter,
        order_by: Any = None,
    ) -> list[PostReadResponse] | None:
        query = await self._get_all_posts_query(
            posts_filter=posts_filter,
            order_by=order_by,
            order=IOrderEnum.descendent,
        )
        db_result = (await self.db.execute(query)).fetchall()
        return [
            PostReadResponse(
                id=row[0].id,
                title=row[0].title,
                photo=row[0].photo,
                description=row[0].description,
                owner=UserRead(**row[1])
            ) for row in db_result
        ] if db_result else None

    @staticmethod
    async def _get_all_posts_query(
            posts_filter: PostFilter,
            order_by: Any,
            order: IOrderEnum | None = None,
    ) -> Select:
        owner = aliased(User, name="owner")
        query = (
            select(Post, owner)
            .join(User, User.id == Post.owner)  # type: ignore
            .where(
                and_(
                    or_(not posts_filter.owner, Post.owner == posts_filter.owner),
                    or_(not posts_filter.title, Post.title == posts_filter.title),
                )
            )
        )

        if order == IOrderEnum.ascendent:
            query = query.order_by(order_by.asc())
        else:
            query = query.order_by(order_by.desc())  # type: ignore

        return query
