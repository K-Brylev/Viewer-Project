import strawberry
from typing import Optional, List
from enum import Enum

@strawberry.type
class ItemType:
    id: int
    name: str
    description:str
    icon:str
    patch:Optional[float]
    category:str
    sub_category:str
    outdoor:bool
    tradeable:bool
    dyeable:bool
    tags: Optional[str]

@strawberry.type
class ItemPage:
    has_more: bool
    items: List[ItemType]

@strawberry.enum
class ItemCategory(Enum):
    TABLE = "Table"
    OTDRFURN = "Outdoor Furnishing"
    TABLETOP = "Tabletop"
    RUG = "Rug"
    WALLMNTD = "Wall-mounted"
    FURNISHING = "Furnishing"
    INTRFIX = "Interior Fixtures"
    EXTRFIX = "Exterior Fixtures"

@strawberry.input
class ItemFilter:
    search: Optional[str] = None
    categories: Optional[List[ItemCategory]] = None
    outdoor: Optional[bool] = None
    tradeable: Optional[bool] = None
    dyeable: Optional[bool] = None