from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, Date, Boolean, ForeignKey
from app.db import Base
from datetime import datetime, date
import enum

class EntryType(enum.Enum):
    note = "note"
    idea = "idea"
    reflection = "reflection"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    receive_prompts = Column(Boolean, default=True)
    channel = Column(String, default="telegram")  # allows extension in future

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    message_id = Column(Integer)
    username = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    text = Column(Text, nullable=False)
    entry_type = Column(Enum(EntryType), nullable=False)
    tags = Column(String, nullable=True)
    source = Column(String, nullable=False, default="manual")
    date_only = Column(Date, default=date.today)
