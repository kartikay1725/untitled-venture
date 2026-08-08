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
async def test_submit_and_retrieve_idea(async_test_client):
    payload = {"email": "idea@example.com", "password": "StrongPass123"}
    reg = await async_test_client.post("/api/auth/register", json=payload)
    token = reg.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    idea_payload = {"description": "A revolutionary app that does X"}
    resp = await async_test_client.post("/api/ideas", json=idea_payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    idea_id = data["idea_id"]
    get_resp = await async_test_client.get(f"/api/ideas/{idea_id}/validation", headers=headers)
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    assert get_data["idea_id"] == idea_id