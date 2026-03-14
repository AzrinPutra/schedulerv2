"""Console setup for TUI."""

from rich.console import Console
from .theme import THEME

console = Console(
    theme=THEME,
)

def get_console() -> Console:
    """Get the configured console instance."""
    return console
