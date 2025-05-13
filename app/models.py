from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, Date
from app.db import Base
from datetime import datetime, date
import enum

class EntryType(enum.Enum):
    note = "note"
    idea = "idea"
    reflection = "reflection"

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    message_id = Column(Integer)
    username = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    text = Column(Text, nullable=False)
    entry_type = Column(Enum(EntryType), nullable=False)
    tags = Column(String, nullable=True)
    source = Column(String, nullable=False, default="manual")
    date_only = Column(Date, default=date.today)
