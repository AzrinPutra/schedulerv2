"""Schedule data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Optional
from uuid import uuid4
from .enums import Category, Priority, Status
from .validation import (
    validate_uuid, validate_date, validate_optional_time, 
    validate_positive_int, validate_enum, validate_non_empty_string
)
from .serialization import (
    datetime_to_iso, datetime_from_iso,
    date_to_iso, date_from_iso,
    time_to_iso, time_from_iso,
    enum_to_value, enum_from_value
)


@dataclass
class BaseModel:
    """Abstract base model with common attributes."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the model after initialization."""
        self.validate()

    def validate(self):
        """Validate the model fields."""
        self.id = validate_uuid(self.id, "id")

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "created_at": datetime_to_iso(self.created_at),
            "updated_at": datetime_to_iso(self.updated_at),
        }

    @classmethod
    def from_dict(cls, data: dict) -> BaseModel:
        """Create model from dictionary."""
        return cls(
            id=data.get("id") or str(uuid4()),
            created_at=datetime_from_iso(data.get("created_at")) or datetime.now(),
            updated_at=datetime_from_iso(data.get("updated_at")) or datetime.now(),
        )


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
        """Update the updated_at timestamp and validate."""
        super().__post_init__()
        self.updated_at = datetime.now()

    def validate(self):
        """Validate the model fields."""
        super().validate()
        self.title = validate_non_empty_string(self.title, "title")
        if self.due_date is not None:
            self.due_date = validate_date(self.due_date, "due_date")
        if self.category is not None:
            validate_enum(self.category, Category, "category")
        if self.priority is not None:
            validate_enum(self.priority, Priority, "priority")
        if self.status is not None:
            validate_enum(self.status, Status, "status")

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            **super().to_dict(),
            "title": self.title,
            "description": self.description,
            "due_date": date_to_iso(self.due_date),
            "category": enum_to_value(self.category),
            "priority": enum_to_value(self.priority),
            "status": enum_to_value(self.status),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        """Create model from dictionary."""
        return cls(
            id=data.get("id") or str(uuid4()),
            created_at=datetime_from_iso(data.get("created_at")) or datetime.now(),
            updated_at=datetime_from_iso(data.get("updated_at")) or datetime.now(),
            title=data.get("title", ""),
            description=data.get("description"),
            due_date=date_from_iso(data.get("due_date")),
            category=enum_from_value(data.get("category"), Category) or Category.PERSONAL,
            priority=enum_from_value(data.get("priority"), Priority) or Priority.MEDIUM,
            status=enum_from_value(data.get("status"), Status) or Status.PENDING,
        )


@dataclass
class Event(BaseModel):
    """Represents a scheduled event."""
    
    title: str = ""
    description: Optional[str] = None
    date_field: date = field(default_factory=date.today)
    category: Category = Category.PERSONAL
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    time: Optional[time] = None
    duration_minutes: Optional[int] = None
    
    def __post_init__(self):
        """Update the updated_at timestamp and validate."""
        super().__post_init__()
        self.updated_at = datetime.now()

    def validate(self):
        """Validate the model fields."""
        super().validate()
        self.title = validate_non_empty_string(self.title, "title")
        self.date_field = validate_date(self.date_field, "date")
        if self.time is not None:
            validate_optional_time(self.time, "time")
        if self.duration_minutes is not None:
            validate_positive_int(self.duration_minutes, "duration_minutes")
        if self.category is not None:
            validate_enum(self.category, Category, "category")
        if self.priority is not None:
            validate_enum(self.priority, Priority, "priority")
        if self.status is not None:
            validate_enum(self.status, Status, "status")

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            **super().to_dict(),
            "title": self.title,
            "description": self.description,
            "date": date_to_iso(self.date_field),
            "category": enum_to_value(self.category),
            "priority": enum_to_value(self.priority),
            "status": enum_to_value(self.status),
            "time": time_to_iso(self.time),
            "duration_minutes": self.duration_minutes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Event:
        """Create model from dictionary."""
        return cls(
            id=data.get("id") or str(uuid4()),
            created_at=datetime_from_iso(data.get("created_at")) or datetime.now(),
            updated_at=datetime_from_iso(data.get("updated_at")) or datetime.now(),
            title=data.get("title", ""),
            description=data.get("description"),
            date_field=date_from_iso(data.get("date")) or date.today(),
            category=enum_from_value(data.get("category"), Category) or Category.PERSONAL,
            priority=enum_from_value(data.get("priority"), Priority) or Priority.MEDIUM,
            status=enum_from_value(data.get("status"), Status) or Status.PENDING,
            time=time_from_iso(data.get("time")),
            duration_minutes=data.get("duration_minutes"),
        )


@dataclass
class ScheduleItem(BaseModel):
    """Represents an item in the schedule."""
    
    title: str = ""
    description: Optional[str] = None
    date_field: date = field(default_factory=date.today)
    category: Category = Category.PERSONAL
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    time: Optional[time] = None
    duration_minutes: Optional[int] = None
    task_id: Optional[str] = None
    event_id: Optional[str] = None
    
    def __post_init__(self):
        """Update the updated_at timestamp and validate."""
        super().__post_init__()
        self.updated_at = datetime.now()

    def validate(self):
        """Validate the model fields."""
        super().validate()
        self.title = validate_non_empty_string(self.title, "title")
        self.date_field = validate_date(self.date_field, "date")
        if self.time is not None:
            validate_optional_time(self.time, "time")
        if self.duration_minutes is not None:
            validate_positive_int(self.duration_minutes, "duration_minutes")
        if self.task_id is not None:
            validate_uuid(self.task_id, "task_id")
        if self.event_id is not None:
            validate_uuid(self.event_id, "event_id")
        if self.category is not None:
            validate_enum(self.category, Category, "category")
        if self.priority is not None:
            validate_enum(self.priority, Priority, "priority")
        if self.status is not None:
            validate_enum(self.status, Status, "status")

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            **super().to_dict(),
            "title": self.title,
            "description": self.description,
            "date": date_to_iso(self.date_field),
            "category": enum_to_value(self.category),
            "priority": enum_to_value(self.priority),
            "status": enum_to_value(self.status),
            "time": time_to_iso(self.time),
            "duration_minutes": self.duration_minutes,
            "task_id": self.task_id,
            "event_id": self.event_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> ScheduleItem:
        """Create model from dictionary."""
        return cls(
            id=data.get("id") or str(uuid4()),
            created_at=datetime_from_iso(data.get("created_at")) or datetime.now(),
            updated_at=datetime_from_iso(data.get("updated_at")) or datetime.now(),
            title=data.get("title", ""),
            description=data.get("description"),
            date_field=date_from_iso(data.get("date")) or date.today(),
            category=enum_from_value(data.get("category"), Category) or Category.PERSONAL,
            priority=enum_from_value(data.get("priority"), Priority) or Priority.MEDIUM,
            status=enum_from_value(data.get("status"), Status) or Status.PENDING,
            time=time_from_iso(data.get("time")),
            duration_minutes=data.get("duration_minutes"),
            task_id=data.get("task_id"),
            event_id=data.get("event_id"),
        )
