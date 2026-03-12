from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.database.database import get_db, init_db
from app.graphql.schema import schema
from app.services.xivapi import ingest_items

app = FastAPI(title="FFXIV Housing API")

async def get_context(db=Depends(get_db)):
    return {"db": db}

graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message":"Welcome to the FFXIV Housing API"}

@app.post("/ingest")
async def ingest(db:AsyncSession = Depends(get_db)):
    await init_db()
    items = await ingest_items(db)
    return {"count": len(items), "items": items}