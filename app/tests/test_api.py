import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    res = client.post("/api/auth/register", json={"email": "api@test.com", "password": "Password123!"})
    assert res.status_code == 200
    token = res.json()["token"]
    res = client.post("/api/auth/login", json={"email": "api@test.com", "password": "Password123!"})
    assert res.status_code == 200
    assert res.json()["token"] == token

def test_idea_flow():
    # Register
    res = client.post("/api/auth/register", json={"email": "flow@test.com", "password": "Password123!"})
    token = res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Submit idea
    res = client.post("/api/ideas", json={"description": "A platform for remote teams."}, headers=headers)
    assert res.status_code == 200
    idea_id = res.json()["idea_id"]
    # Get validation
    res = client.get(f"/api/ideas/{idea_id}/validation", headers=headers)
    assert res.status_code == 200
    assert "validation_score" in res.json()

def test_mvp_flow():
    # Register
    res = client.post("/api/auth/register", json={"email": "mvpflow@test.com", "password": "Password123!"})
    token = res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Submit idea
    res = client.post("/api/ideas", json={"description": "An AI chatbot for customer support."}, headers=headers)
    idea_id = res.json()["idea_id"]
    # Generate MVP
    res = client.post("/api/mvp", json={"idea_id": idea_id}, headers=headers)
    assert res.status_code == 200
    mvp_id = res.json()["mvp_id"]
    # Download
    res = client.get(f"/api/mvp/{mvp_id}/download", headers=headers)
    assert res.status_code == 200
    assert "zip_url" in res.json()
