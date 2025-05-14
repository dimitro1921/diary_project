import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import get_db, Base
from app import models
from api.main import app

# ------------------------
# Create test engine
# ------------------------

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ------------------------
# Override dependency
# ------------------------

@pytest.fixture(scope="module")
def client():
    # Create all tables using the real Base from app.db
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    Base.metadata.drop_all(bind=engine)

# -------- Tests --------

def test_create_entry(client):
    data = {
        "user_id": 1,
        "message_id": 101,
        "username": "tester",
        "text": "API test entry",
        "entry_type": "note",
        "tags": "#api,#test",
        "source": "manual",
        "date_only": "2025-05-14"
    }
    response = client.post("/entry", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["text"] == "API test entry"
    assert result["entry_type"] == "note"

def test_get_entries_by_date(client):
    response = client.get("/entry/2025-05-14?user_id=1")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert result[0]["text"] == "API test entry"

def test_list_recent_entries(client):
    response = client.get("/list?user_id=1&limit=2")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) <= 2

def test_export_entries(client):
    response = client.get("/export?user_id=1&start_date=2025-05-01&end_date=2025-05-20")
    assert response.status_code == 200
    result = response.json()
    assert "markdown" in result
    assert "# 📓" in result["markdown"]


# -------- USER TESTS --------

def test_create_user(client):
    data = {
        "telegram_id": 999999,
        "username": "testuser",
        "receive_prompts": True,
        "channel": "telegram"
    }
    response = client.post("/users", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["telegram_id"] == 999999
    assert result["username"] == "testuser"
    global created_user_id
    created_user_id = result["id"]

def test_get_user(client):
    response = client.get(f"/users/{created_user_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == created_user_id
    assert result["telegram_id"] == 999999

def test_update_user(client):
    update_data = {
        "receive_prompts": False
    }
    response = client.patch(f"/users/{created_user_id}", json=update_data)
    assert response.status_code == 200
    result = response.json()
    assert result["receive_prompts"] is False

def test_delete_user(client):
    response = client.delete(f"/users/{created_user_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == "User deleted"

    # Confirm deletion
    confirm = client.get(f"/users/{created_user_id}")
    assert confirm.status_code == 404
