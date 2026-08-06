import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_register_and_login():
    resp = client.post("/api/auth/register", json={"email": "user@example.com", "password": "Passw0rd!"})
    assert resp.status_code == 201
    resp = client.post("/api/auth/login", data={"username": "user@example.com", "password": "Passw0rd!"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert token
