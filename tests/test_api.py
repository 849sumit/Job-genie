from pathlib import Path

from fastapi.testclient import TestClient

from job_genie_backend.app import app

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = ROOT_DIR / "job_genie.db"

if DB_FILE.exists():
    DB_FILE.unlink()

client = TestClient(app)


def test_signup_creates_user() -> None:
    payload = {
        "email": "test-user@example.com",
        "full_name": "Test User",
        "password": "secure-password",
    }

    response = client.post("/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert "id" in data
