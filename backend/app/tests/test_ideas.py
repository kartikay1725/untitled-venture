def test_idea_submission(client):
    payload = {"email": "user@example.com", "password": "password123"}
    client.post("/api/auth/register", json=payload)
    login = client.post("/api/auth/login", json=payload).json()
    token = login["token"]
    headers = {"Authorization": f"Bearer {token}"}
    idea_payload = {"description": "Test idea description"}
    r = client.post("/api/ideas/", json=idea_payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert "validation_score" in data