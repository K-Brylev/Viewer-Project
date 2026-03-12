import strawberry
from typing import Optional, List
from enum import Enum

@strawberry.type
class ItemType:
    id: int
    name: str
    description:str
    patch:Optional[float]
    category:str
    sub_category:str
    outdoor:bool
    tradeable:bool
    dyeable:bool
    tags: Optional[str]

@strawberry.enum
class ItemCategory(Enum):
    TABLE = "Tables"
    OTDRFURN = "Outdoor Furnishings"
    TABLETOP = "Tabletop"
    RUG = "Rugs"
    WALLMNTD = "Wall-mounted"
    CHAIRBED = "Chairs and Beds"
    PAINTING = "Paintings"
    FURNISHING = "Furnishings"
    INTRFIX = "Interior Fixtures"
    EXTRFIX = "Exterior Fixtures"

@strawberry.input
class ItemFilter:
    search: Optional[str] = None
    categories: Optional[List[ItemCategory]] = None
    outdoor: Optional[bool] = None
    tradeable: Optional[bool] = None
    dyeable: Optional[bool] = None