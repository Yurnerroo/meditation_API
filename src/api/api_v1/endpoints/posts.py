from fastapi import APIRouter, Depends, HTTPException

from api.api_v1.endpoints.users import FORBIDDEN
from api.deps import PostCrudSession, CurrentActiveUser, CurrentSuperUser
from db.models.post import Post
from db.schemas.post_schema import (
    PostCreate,
    PostRead,
    PostReadResponse,
    PostUpdate,
    PostAdminUpdate,
    PostAdminCreate, PostFilter,
)

router = APIRouter()
POST_NOT_FOUND = HTTPException(status_code=404, detail="Post doesn't exist.")


@router.get("/{post_id}", response_model=PostReadResponse)
async def get_post_by_id(
    post_id: int,
    post_crud: PostCrudSession,
):
    post = await post_crud.get_post(post_id=post_id)
    if not post:
        raise POST_NOT_FOUND
    return PostRead.from_orm(post)


@router.post("/")
async def create_post(
    post: PostCreate,
    current_user: CurrentActiveUser,
    post_crud: PostCrudSession,
):
    return await post_crud.create_post(
        post_in=post,
        current_user=current_user,
    )


@router.put("/{post_id}")
async def update_post(
    post_id: int,
    post_crud: PostCrudSession,
    current_user: CurrentActiveUser,
    post_in: PostUpdate = Depends(),
):
    post = await post_crud.get(id_=post_id)
    if not post:
        raise POST_NOT_FOUND

    if not current_user.id == post.owner:
        raise FORBIDDEN

    return await post_crud.update(
        db_obj=post,
        obj_in=post_in,
    )


@router.post("/admin/")
async def create_post_admin(
    post: PostAdminCreate,
    current_super_user: CurrentSuperUser,
    post_crud: PostCrudSession,
):
    return await post_crud.create_post_admin(
        post_in=post,
        current_user=current_super_user,
    )


@router.put("/admin/{post_id}")
async def update_post_admin(
        post_id: int,
        post_crud: PostCrudSession,
        _current_super_user: CurrentSuperUser,
        post_in: PostAdminUpdate = Depends(),
):
    post = await post_crud.get(id_=post_id)
    if not post:
        raise POST_NOT_FOUND

    return await post_crud.update(
        db_obj=post,
        obj_in=post_in,
    )


@router.get("/", response_model=list[PostReadResponse] | None)
async def get_all_posts(
    post_crud: PostCrudSession,
    posts_filter: PostFilter = Depends(),
) -> list[PostReadResponse] | None:
    """
    Retrieve all users.
    """
    return await post_crud.get_all_posts_ordered(
        posts_filter=posts_filter,
        order_by=Post.time,
    )
