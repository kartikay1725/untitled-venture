import pytest
from httpx import AsyncClient
from app.main import app
import uuid

@pytest.mark.asyncio
async def test_idea_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/api/auth/register", json={"email":"idea@example.com","password":"StrongPass123"})
        resp = await ac.post("/api/auth/login", json={"email":"idea@example.com","password":"StrongPass123"})
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        idea_resp = await ac.post("/api/ideas", json={"description":"A new AI idea","industry_tags":["AI","ML"]}, headers=headers)
        assert idea_resp.status_code == 200
        idea_id = uuid.UUID(idea_resp.json()["id"])
        val_resp = await ac.get(f"/api/ideas/{idea_id}/validation", headers=headers)
        assert val_resp.status_code == 200
        data = val_resp.json()
        assert "validationScore" in data
        assert "recommendedFeatures" in data
