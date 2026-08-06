import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.services.user_service import UserService
from backend.api.schemas.auth import UserCreate

@pytest.fixture
async def async_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
    await engine.dispose()

@pytest.mark.asyncio
async def test_create_user(async_db):
    service = UserService(async_db)
    user_in = UserCreate(email="test@example.com", password="Password123!")
    user = await service.create_user(user_in)
    assert user.email == "test@example.com"
    assert user.id is not None
