import os
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register
        resp = await ac.post("/api/auth/register", json={"email": "test@example.com", "password": "StrongPass1"})
        assert resp.status_code == 201
        token = resp.json()["access_token"]
        assert token
        # Login
        resp = await ac.post("/api/auth/login", data={"username": "test@example.com", "password": "StrongPass1"})
        assert resp.status_code == 200
        assert resp.json()["access_token"]

@pytest.mark.asyncio
async def test_idea_and_mvp_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register and get token
        await ac.post("/api/auth/register", json={"email": "idea@example.com", "password": "StrongPass1"})
        login = await ac.post("/api/auth/login", data={"username": "idea@example.com", "password": "StrongPass1"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Submit idea
        idea_resp = await ac.post("/api/ideas", json={"description": "Test idea", "industry_tags": ["tech"]}, headers=headers)
        assert idea_resp.status_code == 200
        idea_id = idea_resp.json()["id"]
        # Generate MVP
        mvp_resp = await ac.post("/api/mvp", json={"idea_id": idea_id, "features": ["Login", "Dashboard"]}, headers=headers)
        assert mvp_resp.status_code == 200
        mvp_id = mvp_resp.json()["id"]
        # Retrieve MVP
        get_resp = await ac.get(f"/api/mvp/{mvp_id}", headers=headers)
        assert get_resp.status_code == 200
        assert get_resp.json()["generated_code"] is not None

@pytest.mark.asyncio
async def test_deployment_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/api/auth/register", json={"email": "deploy@example.com", "password": "StrongPass1"})
        login = await ac.post("/api/auth/login", data={"username": "deploy@example.com", "password": "StrongPass1"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        idea_resp = await ac.post("/api/ideas", json={"description": "Deploy idea", "industry_tags": ["cloud"]}, headers=headers)
        idea_id = idea_resp.json()["id"]
        mvp_resp = await ac.post("/api/mvp", json={"idea_id": idea_id, "features": ["Auth", "API"]}, headers=headers)
        mvp_id = mvp_resp.json()["id"]
        dep_resp = await ac.post("/api/deploy", json={"mvp_id": mvp_id, "target": "vercel"}, headers=headers)
        assert dep_resp.status_code == 200
        dep_id = dep_resp.json()["id"]
        status_resp = await ac.get(f"/api/deployments/{dep_id}", headers=headers)
        assert status_resp.json()["status"] == "success"
