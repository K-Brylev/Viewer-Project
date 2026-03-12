import strawberry
from typing import List
from app.graphql.resolvers import resolve_items
from app.graphql.types import ItemPage

@strawberry.type
class Query:
    page:ItemPage = strawberry.field(resolver=resolve_items)
        

schema = strawberry.Schema(query=Query)