import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.main import app
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models import Base
import os

@pytest.fixture(scope="session")
async def async_client():
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(os.environ["DATABASE_URL"], future=True, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register_and_login(async_client):
    resp = await async_client.post("/api/auth/register", json={"email": "test@example.com", "password": "secret"})
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    login_resp = await async_client.post("/api/auth/login", json={"email": "test@example.com", "password": "secret"})
    assert login_resp.status_code == 200
    assert login_resp.json()["token"] == data["token"]

@pytest.mark.asyncio
async def test_idea_flow(async_client):
    # Register and login
    await async_client.post("/api/auth/register", json={"email": "user@example.com", "password": "pass"})
    login = await async_client.post("/api/auth/login", json={"email": "user@example.com", "password": "pass"})
    token = login.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Submit idea
    idea_resp = await async_client.post("/api/ideas", json={"description": "A new app idea for entrepreneurs"}, headers=headers)
    assert idea_resp.status_code == 200
    idea_id = idea_resp.json()["idea_id"]
    # Get validation
    val_resp = await async_client.get(f"/api/ideas/{idea_id}/validation", headers=headers)
    assert val_resp.status_code == 200
    # Generate MVP (should fail because score < 70)
    mvp_resp = await async_client.post("/api/mvp", json={"idea_id": idea_id}, headers=headers)
    assert mvp_resp.status_code == 400