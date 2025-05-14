from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app import crud, schemas
from app.db import get_db
from app.exporter import entries_to_markdown

router = APIRouter()

@router.post("/entry", response_model=schemas.EntryOut)
def create_entry(entry: schemas.EntryIn, db: Session = Depends(get_db)):
    """
    Create a new diary entry.
    """
    return crud.create_entry(db, entry)


@router.get("/entry/{entry_date}", response_model=List[schemas.EntryOut])
def read_entries_by_date(entry_date: date, user_id: int, db: Session = Depends(get_db)):
    """
    Get all entries for a specific user and date.
    """
    entries = crud.get_entries_by_date(db, user_id, entry_date)
    return [schemas.EntryOut.model_validate(e) for e in entries]


@router.get("/list", response_model=List[schemas.EntryOut])
def list_recent_entries(user_id: int, limit: int = Query(5, le=50), db: Session = Depends(get_db)):
    """
    Get recent entries for a user.
    """
    entries = crud.list_recent_entries(db, user_id, limit)
    return [schemas.EntryOut.model_validate(e) for e in entries]


@router.get("/export")
def export_entries(user_id: int,
                   start_date: Optional[date] = None,
                   end_date: Optional[date] = None,
                   db: Session = Depends(get_db)):
    """
    Export entries as a Markdown-formatted string.
    """
    entries = crud.export_entries(db, user_id, start_date, end_date)
    if not entries:
        return {"message": "No entries found in the given date range."}

    entries_out = [schemas.EntryOut.model_validate(e) for e in entries]
    markdown = entries_to_markdown(entries_out)
    return {"markdown": markdown}
