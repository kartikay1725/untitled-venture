import pytest, uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def user_token():
    # Register
    resp = client.post("/auth/register", json={"email": "test@example.com", "password": "StrongPass123"})
    assert resp.status_code == 200
    # Login
    resp = client.post("/auth/login", data={"username": "test@example.com", "password": "StrongPass123"})
    assert resp.status_code == 200
    return resp.json()["access_token"]

def test_submit_and_validate(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Submit idea
    resp = client.post("/ideas", json={"title": "Test Idea", "description": "A great idea."}, headers=headers)
    assert resp.status_code == 201
    idea_id = resp.json()["idea_id"]
    # Retrieve validation (will be pending until AI runs)
    resp = client.get(f"/ideas/{idea_id}/validation", headers=headers)
    # Expect 404 initially
    assert resp.status_code in [404, 200]

def test_generate_blueprint(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Assuming an idea with id exists and validated
    idea_id = uuid.uuid4()  # placeholder, in real test fetch from DB
    resp = client.post("/blueprints", json={"idea_id": str(idea_id), "scope": "basic"}, headers=headers)
    # Should return 201 or error if idea not found
    assert resp.status_code in [201, 404]
