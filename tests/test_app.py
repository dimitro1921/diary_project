import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app import crud, models, schemas
from app.exporter import entries_to_markdown
from datetime import datetime, date

# --- SETUP ---

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

# --- BASE TESTS ---

def test_create_entry(db):
    entry_data = schemas.EntryIn(
        user_id=1,
        message_id=123,
        username="tester",
        text="Test idea entry",
        entry_type=models.EntryType.idea,
        tags="#test",
        source="manual",
        date_only=date.today(),
        timestamp=datetime.utcnow()
    )
    entry = crud.create_entry(db, entry_data)
    assert entry.id is not None
    assert entry.text == "Test idea entry"

def test_get_entries_by_date(db):
    today = date.today()
    results = crud.get_entries_by_date(db, user_id=1, entry_date=today)
    assert len(results) >= 1

def test_list_recent_entries(db):
    entries = crud.list_recent_entries(db, user_id=1, limit=3)
    assert isinstance(entries, list)

def test_entries_to_markdown(db):
    entries = crud.list_recent_entries(db, user_id=1, limit=1)
    md = entries_to_markdown(entries)
    assert "# 📓" in md
    assert "## 📅" in md
    assert "**Type**:" in md

# --- EDGE CASE TESTS ---

def test_create_empty_text_fails():
    with pytest.raises(ValueError):
        schemas.EntryIn(
            user_id=2,
            message_id=999,
            username="tester",
            text="",
            entry_type=models.EntryType.note,
            timestamp=datetime.utcnow()
        )

def test_invalid_entry_type_enum():
    with pytest.raises(ValueError):
        schemas.EntryIn(
            user_id=2,
            message_id=1000,
            username="tester",
            text="This is invalid type",
            entry_type="not_an_enum",
            timestamp=datetime.utcnow()
        )

def test_export_with_start_after_end(db):
    entries = crud.export_entries(
        db,
        user_id=1,
        start_date=date(2030, 1, 1),
        end_date=date(2020, 1, 1)
    )
    assert entries == []

def test_list_recent_entries_for_unknown_user(db):
    entries = crud.list_recent_entries(db, user_id=99999)
    assert entries == []

def test_get_entries_by_date_no_results(db):
    entries = crud.get_entries_by_date(db, user_id=1, entry_date=date(2000, 1, 1))
    assert entries == []
