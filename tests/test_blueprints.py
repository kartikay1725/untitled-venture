import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_blueprint_generation(client):
    await client.post("/auth/register", json={"email":"bp@example.com","password":"StrongPass123!"})
    login_resp = await client.post("/auth/login", data={"username":"bp@example.com","password":"StrongPass123!"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    idea_resp = await client.post("/ideas/", json={"title":"Blueprint Idea","description":"Description for blueprint."}, headers=headers)
    idea_id = idea_resp.json()["id"]
    bp_resp = await client.post("/blueprints/", json={"idea_id":idea_id,"scope":"basic"}, headers=headers)
    assert bp_resp.status_code == 200
    data = bp_resp.json()
    assert "features" in data
    assert "timeline" in data
