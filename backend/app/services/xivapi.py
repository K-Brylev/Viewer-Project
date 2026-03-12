import httpx
import app.services.github as github
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Item

XIVAPI_URL = "https://v2.xivapi.com/api/"
SHEETS = {
    "Indoor": "FurnitureCatalogItemList",
    "Outdoor": "YardCatalogItemList"
}
QUERYS = {
    "Indoor": "ItemSearchCategory.Name=\"Interior Fixtures\"",
    "Outdoor": "ItemSearchCategory.Name=\"Exterior Fixtures\""
}

FIELDS = "Name,Description,ItemSearchCategory.Name,ItemUICategory.Name,Icon,IsUntradable,DyeCount"
FIELDS_EXT = "Category.Category,Item.Name,Item.Description,Item.ItemUICategory.Name,Item.Icon,Item.IsUntradable,Item.DyeCount"


async def fetch_fixtures(filter: str):
    all_results = []
    cursor = None
    async with httpx.AsyncClient() as client:
        while True:
            params={
                "sheets": "Item",
                "query": QUERYS[filter],
                "fields": FIELDS,
                "limit": 500
            }
            if cursor:
                params["cursor"] = cursor
            response = await client.get(
                XIVAPI_URL + "search",
                params=params
            )
            response.raise_for_status()
            data= response.json()

            all_results.extend(data["results"])

            cursor = data.get("next")
            if not cursor:
                break

        print(f"Collected {len(all_results)} items")
        return all_results

async def fetch_extended_categories(sheet:str):
    all_results = []
    after = None
    async with httpx.AsyncClient() as client:
        while True:
            params={
                "fields": FIELDS_EXT,
                "limit": 500,
            }
            if after:
                params["after"] = after
            response = await client.get(
                XIVAPI_URL + "sheet/" + SHEETS[sheet],
                params=params
            )
            response.raise_for_status()
            data= response.json()
            all_results.extend(data["rows"])

            if after:
                after += params["limit"]
            else:
                after = params["limit"] - 1

            if len(all_results) < after:
                break

        return all_results

def create_yard_furniture_item(item, patch_map, is_outdoor: bool):
    item_data = item.get("fields").get("Item")
    item_id = item_data.get("row_id")
    patch = patch_map.get(str(item_id))
    fields = item_data.get("fields")
    new_item = Item(
        id=item_id,
        name=fields.get("Name"),
        description=fields.get("Description"),
        patch=patch,
        category=fields.get("ItemUICategory").get("fields").get("Name"),
        sub_category=item.get("fields").get("Category").get("fields").get("Category"),
        icon=fields.get("Icon", {}).get("path_hr1"),
        outdoor=is_outdoor,
        tradeable=not fields.get("IsUntradable", False),
        dyeable=fields.get("DyeCount", 0) > 0,
        tags=""
    )
    return new_item

def create_fixture_item(item, patch_map, is_outdoor: bool):
    item_id = item.get("row_id")
    patch = patch_map.get(str(item_id))
    fields = item.get("fields")
    new_item = Item(
        id=item_id,
        name=fields.get("Name"),
        description=fields.get("Description"),
        patch=patch,
        category=fields.get("ItemSearchCategory").get("fields").get("Name"),
        sub_category=fields.get("ItemUICategory").get("fields").get("Name"),
        icon=fields.get("Icon", {}).get("path_hr1"),
        outdoor=is_outdoor,
        tradeable=not fields.get("IsUntradable", False),
        dyeable=fields.get("DyeCount", 0) > 0,
        tags=""
    )
    return new_item

async def ingest_items(db:AsyncSession):
    items = []
    patch_map = await github.load_patch_data()
    interior_fixtures = await fetch_fixtures("Indoor")
    exterior_fixtures = await fetch_fixtures("Outdoor")
    indoor_catalog_items = await fetch_extended_categories("Indoor")
    outdoor_catalog_items = await fetch_extended_categories("Outdoor")
    async with db:
        for item in indoor_catalog_items:

            new_item = create_yard_furniture_item(item, patch_map, False)

            items.append(str(new_item))
            await db.merge(new_item)

        for item in outdoor_catalog_items:
            
            new_item = create_yard_furniture_item(item, patch_map, True)

            items.append(str(new_item))
            await db.merge(new_item)

        for item in interior_fixtures:
            
            new_item = create_fixture_item(item, patch_map, False)

            items.append(str(new_item))
            await db.merge(new_item)

        for item in exterior_fixtures:
            
            new_item = create_fixture_item(item, patch_map, True)

            items.append(str(new_item))
            await db.merge(new_item)

        await db.commit()
    return items