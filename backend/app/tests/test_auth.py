import pytest
from httpx import AsyncClient
from app.main import app
from app.db import async_session, Base, engine

@pytest.fixture(scope="module")
async def async_test_client():
    async with async_session() as session:
        async with session.begin():
            await session.run_sync(Base.metadata.create_all)
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    async with async_session() as session:
        async with session.begin():
            await session.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_register_and_login(async_test_client):
    payload = {"email": "test@example.com", "password": "StrongPass123"}
    resp = await async_test_client.post("/api/auth/register", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"

    login_resp = await async_test_client.post("/api/auth/login", json=payload)
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert login_data["token"] == data["token"]