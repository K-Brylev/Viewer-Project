from typing import List
from strawberry.types import Info
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Item
from app.graphql.types import ItemType

async def resolve_items(info: Info) -> List[ItemType]:
    db: AsyncSession = info.context["db"]

    result = await db.execute(select(Item))
    return result.scalars().all()