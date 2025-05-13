from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from typing import List, Optional

from app import models, schemas


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
