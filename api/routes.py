from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app import crud, schemas
from app.db import get_db
from app.exporter import entries_to_markdown

router = APIRouter()

# -------------------- ENTRY ENDPOINTS --------------------

@router.post("/entry", response_model=schemas.EntryOut)
def create_entry(entry: schemas.EntryIn, db: Session = Depends(get_db)):
    # Ensure the user exists
    user = crud.get_user_by_id(db, entry.user_id)
    if not user:
        raise HTTPException(400, "User not found")

    # Create the entry
    return crud.create_entry(db, entry)

@router.get("/entry/{entry_date}", response_model=List[schemas.EntryOut])
def read_entries_by_date(entry_date: date, user_id: int, db: Session = Depends(get_db)):
    """
    Get all entries for a specific user and date.
    """
    entries = crud.get_entries_by_date(db, user_id=user_id, entry_date=entry_date)
    return [schemas.EntryOut.model_validate(e, from_attributes=True) for e in entries]

@router.get("/list", response_model=List[schemas.EntryOut])
def list_recent_entries(user_id: int, limit: int = Query(5, le=50), db: Session = Depends(get_db)):
    """
    Get recent entries for a user.
    """
    entries = crud.list_recent_entries(db, user_id, limit)
    return entries

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


# -------------------- USER ENDPOINTS --------------------

@router.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400,  detail=f"User already exists {e}")

@router.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, updates: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user_by_id(db, user_id, updates)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user_by_id(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@router.get("/users/by_external_id/{external_id}", response_model=schemas.UserOut)
def get_user_by_external_id(external_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_external_id(db, external_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
