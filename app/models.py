from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db import Base
import enum

class EntryType(enum.Enum):
    note = "note"
    idea = "idea"
    reflection = "reflection"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, index=True)  # Telegram user ID
    source = Column(String, default="telegram")  # e.g., "telegram"
    username = Column(String, nullable=True)
    language = Column(String, default="uk")  # локалізація
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    entries = relationship("Entry", back_populates="user")

    __table_args__ = (
        Index("ix_unique_external_source", "external_id", "source", unique=True),
    )

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True)  # на майбутнє
    text = Column(Text, nullable=False)
    entry_type = Column(Enum(EntryType), nullable=False)
    tags = Column(String, nullable=True)
    source = Column(String, default="manual")
    date_only = Column(Date, default=lambda: datetime.now(timezone.utc).date())

    user = relationship("User", back_populates="entries")
