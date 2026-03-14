"""Schedule data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Optional
from uuid import uuid4
from .enums import Category, Priority, Status


@dataclass
class BaseModel:
    """Abstract base model with common attributes."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Task(BaseModel):
    """Represents a task in the scheduler."""
    
    title: str = ""
    description: Optional[str] = None
    due_date: Optional[date] = None
    category: Category = Category.PERSONAL
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    
    def __post_init__(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()


@dataclass
class Event(BaseModel):
    """Represents a scheduled event."""
    
    title: str = ""
    description: Optional[str] = None
    date: date = field(default_factory=date.today)
    category: Category = Category.PERSONAL
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    time: Optional[time] = None
    duration_minutes: Optional[int] = None
    
    def __post_init__(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()


@dataclass
class ScheduleItem(BaseModel):
    """Represents an item in the schedule."""
    
    title: str = ""
    description: Optional[str] = None
    date: date = field(default_factory=date.today)
    category: Category = Category.PERSONAL
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    time: Optional[time] = None
    duration_minutes: Optional[int] = None
    task_id: Optional[str] = None
    event_id: Optional[str] = None
    
    def __post_init__(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()
