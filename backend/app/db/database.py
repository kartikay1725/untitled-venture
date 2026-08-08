from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close():
    await engine.dispose()