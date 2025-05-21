from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date, timezone
from app.models import EntryType


# ------------------------
# USER SCHEMAS
# ------------------------

class UserBase(BaseModel):
    external_id: int
    source: str = "telegram"
    username: Optional[str] = None
    language: str = "uk"

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    username: Optional[str] = None
    source: Optional[str] = None

# ------------------------
# ENTRY SCHEMAS
# ------------------------

class EntryBase(BaseModel):
    text: str
    entry_type: EntryType
    tags: Optional[str] = None
    source: str = "manual"
    date_only: Optional[date] = None
    message_id: Optional[int] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

class EntryIn(EntryBase):
    user_id: int

class EntryOut(EntryBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }


class ExportModel(BaseModel):
    start_date: date
    end_date: date

class UserUpdate(BaseModel):
    username: Optional[str] = None
    source: Optional[str] = None