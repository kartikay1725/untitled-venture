import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_register_and_login(client):
    resp = await client.post("/auth/register", json={"email":"test@example.com","password":"StrongPass123!"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    resp = await client.post("/auth/login", data={"username":"test@example.com","password":"StrongPass123!"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
