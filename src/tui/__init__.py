"""TUI components using Rich."""

from .console import console, get_console
from .theme import PRIORITY_COLORS, STATUS_COLORS, CATEGORY_COLORS

__all__ = [
    "console",
    "get_console",
    "PRIORITY_COLORS",
    "STATUS_COLORS",
    "CATEGORY_COLORS",
]
