"""Validation utilities for the scheduler models."""

from datetime import date, time
from typing import Any
from uuid import UUID
from .enums import Category, Priority, Status


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_uuid(value: str, field_name: str = "id") -> str:
    """Validate that a value is a valid UUID."""
    try:
        UUID(value)
        return value
    except ValueError:
        raise ValidationError(f"{field_name} must be a valid UUID, got: {value}")


def validate_date(value: date, field_name: str = "date") -> date:
    """Validate that a value is a valid date."""
    if not isinstance(value, date):
        raise ValidationError(f"{field_name} must be a date object, got: {type(value).__name__}")
    return value


def validate_optional_time(value: time, field_name: str = "time") -> time:
    """Validate that a value is a valid time or None."""
    if value is not None and not isinstance(value, time):
        raise ValidationError(f"{field_name} must be a time object or None, got: {type(value).__name__}")
    return value


def validate_positive_int(value: int, field_name: str = "duration_minutes") -> int:
    """Validate that a value is a positive integer or None."""
    if value is not None and (not isinstance(value, int) or value <= 0):
        raise ValidationError(f"{field_name} must be a positive integer or None, got: {value}")
    return value


def validate_enum(value: Any, enum_type: Any, field_name: str = "enum_field") -> Any:
    """Validate that a value is a valid enum member."""
    if value not in enum_type:
        valid_values = [item.value for item in enum_type]
        raise ValidationError(f"{field_name} must be one of {valid_values}, got: {value}")
    return value


def validate_non_empty_string(value: str, field_name: str = "title") -> str:
    """Validate that a string is not empty (after stripping whitespace)."""
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} must be a non-empty string, got: {value}")
    return value.strip()
