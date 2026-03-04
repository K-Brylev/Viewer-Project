import strawberry
from typing import Optional

@strawberry.type
class ItemType:
    id: int
    name: str
    description:str
    patch:Optional[float]
    category:str
    tradeable:bool
    dyeable:bool
    tags: Optional[str]
