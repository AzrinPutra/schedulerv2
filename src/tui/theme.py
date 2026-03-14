"""Theme and color constants for TUI."""

from rich.theme import Theme
from rich.color import Color

PRIORITY_COLORS = {
    "urgent": "red bold",
    "high": "magenta",
    "medium": "yellow",
    "low": "green",
}

STATUS_COLORS = {
    "pending": "yellow",
    "in_progress": "cyan",
    "completed": "green bold",
    "cancelled": "dim red",
}

CATEGORY_COLORS = {
    "school": "blue",
    "learning": "magenta",
    "exercise": "green",
    "personal": "cyan",
    "work": "white",
    "meeting": "yellow",
}

THEME = Theme({
    "priority.urgent": "red bold",
    "priority.high": "magenta",
    "priority.medium": "yellow",
    "priority.low": "green",
    "status.pending": "yellow",
    "status.in_progress": "cyan",
    "status.completed": "green bold",
    "status.cancelled": "dim red",
    "category.school": "blue",
    "category.learning": "magenta",
    "category.exercise": "green",
    "category.personal": "cyan",
    "category.work": "white",
    "category.meeting": "yellow",
    "title": "bold cyan",
    "header": "bold magenta",
    "subtitle": "dim",
})
