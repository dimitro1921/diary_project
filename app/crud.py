from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from app import models, schemas

# ------------------------
# USER CRUD
# ------------------------

def get_user_by_external_id(db: Session, external_id: int, source: str = "telegram") -> Optional[models.User]:
    """
    Fetch a user by their external ID and source (e.g., Telegram user_id + platform).
    """
    return db.execute(
        select(models.User).where(
            models.User.external_id == external_id,
            models.User.source == source
        )
    ).scalar_one_or_none()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this external_id and source already exists")

def get_or_create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Return an existing user, or create one if not found.
    """
    existing_user = get_user_by_external_id(db, user.external_id, user.source)
    if existing_user:
        return existing_user
    return create_user(db, user)

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """
    Fetch a user by internal ID (primary key).
    """
    return db.execute(
        select(models.User).where(models.User.id == user_id)
    ).scalar_one_or_none()

def update_user_by_id(db: Session, user_id: int, updates: schemas.UserUpdate) -> Optional[models.User]:
    """
    Update a user's data by internal ID.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def delete_user_by_id(db: Session, user_id: int) -> bool:
    """
    Delete a user by internal ID.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True

def deactivate_user(db: Session, user_id: int) -> bool:
    """
    Mark user as inactive instead of deleting.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    user.is_active = False
    db.commit()
    return True


# ------------------------
# ENTRY CRUD
# ------------------------

def create_entry(db: Session, entry: schemas.EntryIn) -> models.Entry:
    """
    Create and store a new diary entry in the database.
    """
    db_entry = models.Entry(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_entries_by_date(db: Session, user_id: int, entry_date: date) -> List[models.Entry]:
    """
    Retrieve all entries for a specific user and date.
    """
    return db.execute(
        select(models.Entry).where(
            models.Entry.user_id == user_id,
            models.Entry.date_only == entry_date
        )
    ).scalars().all()

def list_recent_entries(db: Session, user_id: int, limit: int = 5) -> List[models.Entry]:
    """
    Get the most recent entries for a user, limited by count.
    """
    return db.execute(
        select(models.Entry)
        .where(models.Entry.user_id == user_id)
        .order_by(models.Entry.timestamp.desc())
        .limit(limit)
    ).scalars().all()

def export_entries(
    db: Session,
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[models.Entry]:
    """
    Export all entries for a user between start_date and end_date (inclusive).
    """
    query = select(models.Entry).where(models.Entry.user_id == user_id)

    if start_date:
        query = query.where(models.Entry.date_only >= start_date)
    if end_date:
        query = query.where(models.Entry.date_only <= end_date)

    return db.execute(query.order_by(models.Entry.date_only)).scalars().all()
