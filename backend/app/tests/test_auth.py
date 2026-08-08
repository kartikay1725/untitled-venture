import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..db import get_db
from ..models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    from ..models import Base
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_register_and_login(client):
    resp = client.post("/api/auth/register", json={"email":"test@example.com","password":"Password123!"})
    assert resp.status_code == 201
    data = resp.json()
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"

    resp = client.post("/api/auth/login", json={"email":"test@example.com","password":"Password123!"})
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data