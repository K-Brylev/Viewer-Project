from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.database.models import Base
import asyncio
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://test:test@ffxiv_db:5432/ffxiv_db")
engine = create_async_engine(DATABASE_URL,echo=True)

SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS items CASCADE"))

        await conn.run_sync(Base.metadata.create_all)

        await conn.execute(text("ALTER TABLE items DROP COLUMN IF EXISTS search_vector;"))

        await conn.execute(text("""
        ALTER TABLE items
        ADD COLUMN search_vector tsvector GENERATED ALWAYS AS (
            setweight(to_tsvector('english', coalesce(name,'')), 'A') ||
            setweight(to_tsvector('english', coalesce(description,'')), 'B') ||
            setweight(to_tsvector('english', coalesce(tags,'')), 'C') ||
            setweight(to_tsvector('english', coalesce(category,'')), 'D') ||
            setweight(to_tsvector('english', coalesce(sub_category,'')), 'D')
        ) STORED;
        """))

        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_item_search ON items USING GIN(search_vector);
        """))

if __name__ == "__main__":
    asyncio.run(init_db())