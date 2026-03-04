import strawberry
from typing import List
from app.graphql.resolvers import resolve_items
from app.graphql.types import ItemType

@strawberry.type
class Query:
    items:List[ItemType] = strawberry.field(resolver=resolve_items)
        

schema = strawberry.Schema(query=Query)