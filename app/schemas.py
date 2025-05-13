from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime, date
from app.models import EntryType

class EntryBase(BaseModel):
    text: str = Field(..., min_length=1)
    entry_type: EntryType
    tags: Optional[str] = None
    source: str = "manual"
    date_only: Optional[date] = None

class EntryIn(EntryBase):
    user_id: int
    message_id: int
    username: Optional[str] = None
    timestamp: Optional[datetime] = None

class EntryOut(EntryBase):
    id: int
    user_id: int
    message_id: int
    username: Optional[str]
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class ExportModel(BaseModel):
    start_date: date
    end_date: date
