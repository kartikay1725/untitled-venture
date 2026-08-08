def test_mvp_generation(client):
    payload = {"email": "mvp@example.com", "password": "password123"}
    client.post("/api/auth/register", json=payload)
    login = client.post("/api/auth/login", json=payload).json()
    token = login["token"]
    headers = {"Authorization": f"Bearer {token}"}
    idea_payload = {"description": "Generate MVP for this idea"}
    r = client.post("/api/ideas/", json=idea_payload, headers=headers)
    idea_id = r.json()["id"]
    r = client.post("/api/mvp/", json={"idea_id": idea_id}, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert "pdf_url" in data
    assert "download_url" in data