import strawberry

@strawberry.type
class ItemType:
    id: int
    name: str
    description:str
    patch:float
    category:str
    tradeable:bool
    dyeable:bool
    tags:str