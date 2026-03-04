import httpx
import re

async def load_patch_data():
    itemRelations = []
    patchRelations = []
    results = {}
    async with httpx.AsyncClient() as client:
        response = await client.get("https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/refs/heads/staging/libs/data/src/lib/json/item-patch.json")
        response.raise_for_status()
        itemRelations = response.json()

        response = await client.get("https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/refs/heads/staging/libs/data/src/lib/json/patch-names.json")
        response.raise_for_status()
        patchRelations = response.json()
        for key,value in itemRelations.items():
            results[key]= float(re.sub(r'[^0-9.]','', patchRelations.get(str(value)).get("version")))

    return results