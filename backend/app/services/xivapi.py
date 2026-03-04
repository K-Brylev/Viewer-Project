import httpx
import json
import asyncio
import app.services.github as github
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Item

XIVAPI_URL = "https://v2.xivapi.com/api/search"
QUERY = "+(ItemSearchCategory.Name=\"Furnishings\" ItemSearchCategory.Name=\"Outdoor Furnishings\" ItemSearchCategory.Name=\"Tables\" ItemSearchCategory.Name=\"Tabletop\" ItemSearchCategory.Name=\"Chairs and Beds\" ItemSearchCategory.Name=\"Wall-mounted\" ItemSearchCategory.Name=\"Rugs\" ItemSearchCategory.Name=\"Paintings\")"

FIELDS = "Name,Description,version,ItemSearchCategory.Name,Icon,IsUntradable,DyeCount"


async def fetch_items():
    all_results = []
    cursor = None
    async with httpx.AsyncClient() as client:
        while True:
            params={
                "sheets": "Item",
                "query": QUERY,
                "fields": FIELDS,
                "limit": 500
            }
            if cursor:
                params["cursor"] = cursor
            response = await client.get(
                XIVAPI_URL,
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

async def ingest_items(db:AsyncSession):
    items = []
    patch_map = await github.load_patch_data()
    fetched_items = await fetch_items()
    async with db:
        for item in fetched_items:
            item_id = item.get("row_id")
            patch = patch_map.get(str(item_id))
            fields = item.get("fields")
            print(f"(id:{item_id},patch:{patch})")
            new_item = Item(
                id=item_id,
                name=fields.get("Name"),
                description=fields.get("Description"),
                patch=patch,
                category=fields.get("ItemSearchCategory").get("fields").get("Name"),
                icon=fields.get("Icon", {}).get("path_hr1"),
                tradable=not fields.get("IsUntradable", False),
                dyeable=fields.get("DyeCount", 0) > 0,
                tags=""
            )

            items.append(str(new_item))
            await db.merge(new_item)
        await db.commit()
    return items