"""Enum definitions for the scheduler."""

from enum import Enum


class Category(Enum):
    """Categories for tasks and events."""
    
    SCHOOL = "school"
    LEARNING = "learning"
    EXERCISE = "exercise"
    PERSONAL = "personal"
    WORK = "work"
    MEETING = "meeting"


class Priority(Enum):
    """Priority levels for tasks and events."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Status(Enum):
    """Status values for tasks and events."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
