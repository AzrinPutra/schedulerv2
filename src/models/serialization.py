"""Serialization utilities for the scheduler models."""

from datetime import date, time, datetime
from typing import Any, Optional, Type, TypeVar
from enum import Enum

T = TypeVar('T', bound=Enum)


def datetime_to_iso(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to ISO format string."""
    if dt is None:
        return None
    return dt.isoformat()


def datetime_from_iso(iso_string: Optional[str]) -> Optional[datetime]:
    """Convert ISO format string to datetime."""
    if iso_string is None:
        return None
    return datetime.fromisoformat(iso_string)


def date_to_iso(d: Optional[date]) -> Optional[str]:
    """Convert date to ISO format string."""
    if d is None:
        return None
    return d.isoformat()


def date_from_iso(iso_string: Optional[str]) -> Optional[date]:
    """Convert ISO format string to date."""
    if iso_string is None:
        return None
    return date.fromisoformat(iso_string)


def time_to_iso(t: Optional[time]) -> Optional[str]:
    """Convert time to ISO format string."""
    if t is None:
        return None
    return t.isoformat()


def time_from_iso(iso_string: Optional[str]) -> Optional[time]:
    """Convert ISO format string to time."""
    if iso_string is None:
        return None
    return time.fromisoformat(iso_string)


def enum_to_value(enum_obj: Optional[Enum]) -> Optional[str]:
    """Convert enum to its value string."""
    if enum_obj is None:
        return None
    return enum_obj.value


def enum_from_value(value: Optional[str], enum_type: Type[T]) -> Optional[T]:
    """Convert value string to enum member."""
    if value is None:
        return None
    return enum_type(value)
