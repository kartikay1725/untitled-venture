import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_idea_submission_and_validation():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register and login
        await ac.post("/api/auth/register", json={"email": "idea@example.com", "password": "StrongPass1"})
        login = await ac.post("/api/auth/login", data={"username": "idea@example.com", "password": "StrongPass1"})
        token = login.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Submit idea
        resp = await ac.post("/api/ideas", json={"description": "A new marketplace for pet supplies"}, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["validation_score"] >= 0