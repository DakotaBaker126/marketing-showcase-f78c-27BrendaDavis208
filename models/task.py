from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from core.database import Base  # Uses mock Base for now; compatible with future SQLAlchemy engine


class Task(Base):
    """
    Task model definition.
    
    Represents an automation task with minimal but extensible fields.
    Designed to work seamlessly with both mock data layer and future real DB mapping.
    All fields are nullable in mock mode; constraints will be enforced in production DB schema.
    
    Note: This model is intentionally lightweight to support rapid prototyping.
          Future extensions (e.g., user_id, priority, tags) can be added here.
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=True, comment="Brief descriptive title of the task")
    description = Column(String(1024), nullable=True, comment="Detailed task description or instructions")
    status = Column(
        String(50),
        nullable=False,
        default="pending",
        comment="Task lifecycle status: pending | running | completed | failed | cancelled",
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True, comment="Soft-delete flag")

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title[:30] + '...' if self.title and len(self.title) > 30 else self.title}', status='{self.status}')>"

    def to_dict(self) -> dict:
        """Convert instance to dict for consistent mock & API response usage."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
        }