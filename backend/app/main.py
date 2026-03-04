from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends
from app.database import get_db, init_db
from app.services.xivapi import ingest_items

app = FastAPI(title="FFXIV Housing API")

@app.get("/")
async def root():
    return {"message":"Welcome to the FFXIV Housing API"}

@app.post("/ingest")
async def ingest(db:AsyncSession = Depends(get_db)):
    await init_db()
    items = await ingest_items(db)
    return {"count": len(items), "items": items}