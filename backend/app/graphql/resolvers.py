from typing import Optional
from strawberry.types import Info
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Item
from app.graphql.types import ItemPage, ItemFilter

async def resolve_items(info: Info, id:Optional[int] = None, filter: Optional[ItemFilter] = None, limit: int = 50, offset: int = 0) -> ItemPage:
    db: AsyncSession = info.context["db"]
    query = select(Item)
    
    if id:
        query = query.where(Item.id == id)
    elif filter:
        if filter.search:
            tsquery = func.plainto_tsquery("english", filter.search)
            rank = func.ts_rank(Item.search_vector, tsquery)
            query = (
                query.where(
                    Item.search_vector.op("@@")(tsquery)
                    | Item.name.ilike(f"%{filter.search}%")
                )
            ).order_by(rank.desc())
        if filter.categories:
            query = query.where(Item.category.in_([c.value for c in filter.categories]))
        if filter.outdoor is not None:
            query = query.where(Item.outdoor == filter.outdoor)
        if filter.tradeable is not None:
            query = query.where(Item.tradeable == filter.tradeable)
        if filter.dyeable is not None:
            query = query.where(Item.dyeable == filter.dyeable)

    query = query.limit(limit + 1).offset(offset)
    result = await db.execute(query)
    data = result.scalars().all()
    has_more = len(data) >= limit
    items = data[:limit]
    return ItemPage(items=items, has_more=has_more)
    