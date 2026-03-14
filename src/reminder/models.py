"""Reminder models and configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum
from uuid import uuid4


class ReminderType(Enum):
    """Types of reminders."""
    DUE_DATE = "due_date"
    EVENT_START = "event_start"
    DAILY_SUMMARY = "daily_summary"


@dataclass
class Reminder:
    """Represents a reminder for a task or event."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    task_id: Optional[str] = None
    event_id: Optional[str] = None
    reminder_type: ReminderType = ReminderType.DUE_DATE
    minutes_before: int = 60
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "event_id": self.event_id,
            "reminder_type": self.reminder_type.value,
            "minutes_before": self.minutes_before,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Reminder:
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid4())),
            task_id=data.get("task_id"),
            event_id=data.get("event_id"),
            reminder_type=ReminderType(data.get("reminder_type", "due_date")),
            minutes_before=data.get("minutes_before", 60),
            enabled=data.get("enabled", True),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
        )


@dataclass
class ReminderConfig:
    """Configuration for reminder system."""
    
    default_minutes_before: int = 60
    notification_enabled: bool = True
    quiet_hours_start: Optional[int] = None
    quiet_hours_end: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "default_minutes_before": self.default_minutes_before,
            "notification_enabled": self.notification_enabled,
            "quiet_hours_start": self.quiet_hours_start,
            "quiet_hours_end": self.quiet_hours_end,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> ReminderConfig:
        """Create from dictionary."""
        return cls(
            default_minutes_before=data.get("default_minutes_before", 60),
            notification_enabled=data.get("notification_enabled", True),
            quiet_hours_start=data.get("quiet_hours_start"),
            quiet_hours_end=data.get("quiet_hours_end"),
        )
    
    def is_quiet_hours(self, hour: int) -> bool:
        """Check if given hour is in quiet hours."""
        if self.quiet_hours_start is None or self.quiet_hours_end is None:
            return False
        if self.quiet_hours_start <= self.quiet_hours_end:
            return self.quiet_hours_start <= hour < self.quiet_hours_end
        else:
            return hour >= self.quiet_hours_start or hour < self.quiet_hours_end
