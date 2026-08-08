import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register
        resp = await ac.post("/api/auth/register", json={"email": "test@example.com", "password": "StrongPass1"})
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data
        # Login
        resp = await ac.post("/api/auth/login", data={"username": "test@example.com", "password": "StrongPass1"})
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data