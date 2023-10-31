from typing import Any
from typing_extensions import TypeAlias

from sqlalchemy.sql import Select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

from fastapi_pagination.api import apply_items_transformer, create_page
from fastapi_pagination.bases import AbstractParams, RawParams
from fastapi_pagination.types import AdditionalData, AsyncItemsTransformer
from fastapi_pagination.utils import verify_params
from fastapi_pagination.ext.sqlalchemy import count_query, _maybe_unique

AsyncConn: TypeAlias = "AsyncSession | AsyncConnection"


def page_to_limit_offset(params: AbstractParams) -> RawParams:
    return params.to_raw_params().as_limit_offset()


async def paginate_func(
    conn: AsyncConn,
    query: Select,
    params: AbstractParams | None = None,
    *,
    count_stmt: Select | None = None,
    transformer: AsyncItemsTransformer | None = None,
    additional_data: AdditionalData = None,
    unique: bool = True,
) -> Any:
    params, _ = verify_params(params, "limit-offset")
    count_q = count_stmt if count_stmt is not None else count_query(query)
    total = await conn.scalar(count_q)
    items = (await conn.execute(query)).scalars()

    items = _maybe_unique(items, unique)
    # Not tested properly
    t_items = apply_items_transformer(items, transformer)

    return create_page(
        t_items,
        total,
        params,
        **(additional_data or {}),
    )
