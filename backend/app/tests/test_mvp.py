import pytest
from httpx import AsyncClient
from app.main import app
from app.db import async_session, Base, engine
import uuid

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
async def test_generate_mvp(async_test_client, monkeypatch):
    payload = {"email": "mvp@example.com", "password": "StrongPass123"}
    reg = await async_test_client.post("/api/auth/register", json=payload)
    token = reg.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    async def mock_validate_idea(description: str) -> float:
        return 85.0
    monkeypatch.setattr("app.services.idea_validation_service.validate_idea", mock_validate_idea)
    idea_payload = {"description": "App that does Y"}
    idea_resp = await async_test_client.post("/api/ideas", json=idea_payload, headers=headers)
    idea_id = idea_resp.json()["idea_id"]
    async def mock_generate_mvp(idea_id: uuid.UUID):
        return {"mvp_id": str(uuid.uuid4()), "pdf_url": "https://s3.amazonaws.com/bucket/blueprint.pdf", "download_url": "https://s3.amazonaws.com/bucket/package.zip"}
    monkeypatch.setattr("app.services.mvp_generation_service.generate_mvp", mock_generate_mvp)
    mvp_resp = await async_test_client.post("/api/mvp", json={"idea_id": idea_id}, headers=headers)
    assert mvp_resp.status_code == 200
    data = mvp_resp.json()
    assert "mvp_id" in data
    assert "pdf_url" in data
    assert "download_url" in data