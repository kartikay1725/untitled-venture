import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_idea():
    payload = {
        "user_id": "user-123",
        "description": "Build an AI MVP generator",
        "industry_tags": ["AI", "Software"]
    }
    response = client.post("/api/ideas/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "idea_id" in data
    assert "validation_score" in data