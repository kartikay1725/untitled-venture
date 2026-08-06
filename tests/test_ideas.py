import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_idea_submission_and_validation(client):
    await client.post("/auth/register", json={"email":"idea@example.com","password":"StrongPass123!"})
    login_resp = await client.post("/auth/login", data={"username":"idea@example.com","password":"StrongPass123!"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.post("/ideas/", json={"title":"Test Idea","description":"This is a test description."}, headers=headers)
    assert resp.status_code == 200
    idea_id = resp.json()["id"]
    val_resp = await client.get(f"/ideas/{idea_id}/validation", headers=headers)
    assert val_resp.status_code == 200
    data = val_resp.json()
    assert data["status"] == "validated"
    assert data["validation_score"] is not None
