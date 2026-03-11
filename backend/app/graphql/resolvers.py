from typing import List, Optional, Dict
from strawberry.types import Info
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Item
from app.graphql.types import ItemType, ItemFilter

async def resolve_items(info: Info, filter: Optional[ItemFilter] = None, limit: int = 50, offset: int = 0) -> List[ItemType]:
    db: AsyncSession = info.context["db"]
    query = select(Item)
    

    if filter:
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
        if filter.tradeable is not None:
            query = query.where(Item.tradeable == filter.tradeable)
        if filter.dyeable is not None:
            query = query.where(Item.dyeable == filter.dyeable)

    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()
    