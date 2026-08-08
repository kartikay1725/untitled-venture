import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from ..db.database import Base
from ..services.auth_service import AuthService
import os

DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/ideaforge_test")
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="module")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_register_and_authenticate(setup_db):
    async with async_session() as session:
        auth_service = AuthService(session)
        user = await auth_service.register("test@example.com", "password")
        assert user.email == "test@example.com"
        auth_user = await auth_service.authenticate("test@example.com", "password")
        assert auth_user.id == user.id