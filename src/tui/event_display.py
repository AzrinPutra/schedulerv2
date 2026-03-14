"""Event display using Rich."""

from typing import List, Dict
from datetime import date, time
from collections import defaultdict

from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich import box as rich_box

from ..models.schedule import Event
from ..models.enums import Priority, Status, Category
from .console import console
from .theme import PRIORITY_COLORS, STATUS_COLORS, CATEGORY_COLORS
from .task_display import get_priority_style, get_status_style, get_category_style


def format_time(t: time) -> str:
    """Format time for display."""
    return t.strftime("%H:%M")


def format_duration(minutes: int) -> str:
    """Format duration for display."""
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    mins = minutes % 60
    if mins == 0:
        return f"{hours}h"
    return f"{hours}h {mins}m"


def group_events_by_date(events: List[Event]) -> Dict[date, List[Event]]:
    """Group events by date."""
    grouped = defaultdict(list)
    for event in events:
        grouped[event.date_field].append(event)
    return dict(sorted(grouped.items()))


def create_event_table(events: List[Event], title: str = "Events") -> Table:
    """Create a Rich Table displaying events."""
    table = Table(
        title=title,
        show_header=True,
        header_style="bold magenta",
        expand=True,
        box=rich_box.SIMPLE,
    )

    table.add_column("Time", width=8, justify="center")
    table.add_column("Title", style="cyan", min_width=15)
    table.add_column("Duration", width=10, justify="center")
    table.add_column("Category", width=12, justify="center")
    table.add_column("Priority", width=10, justify="center")

    sorted_events = sorted(
        events,
        key=lambda e: (e.time or time(0, 0), e.priority.value)
    )

    for event in sorted_events:
        time_text = Text(
            format_time(event.time) if event.time else "-",
            style="bold cyan"
        )
        
        title_text = Text(event.title)
        
        duration_text = Text(
            format_duration(event.duration_minutes) if event.duration_minutes else "-"
        )
        
        category_text = Text(
            event.category.value.capitalize(),
            style=get_category_style(event.category)
        )
        
        priority_text = Text(
            event.priority.value.upper(),
            style=get_priority_style(event.priority)
        )
        
        table.add_row(
            time_text,
            title_text,
            duration_text,
            category_text,
            priority_text,
        )

    return table


def display_events(events: List[Event], title: str = "Events") -> None:
    """Display events grouped by date."""
    if not events:
        console.print("[dim]No events to display[/dim]")
        return
    
    grouped = group_events_by_date(events)
    
    for event_date, date_events in grouped.items():
        date_str = _format_date_header(event_date)
        table = create_event_table(date_events, date_str)
        console.print(table)
        console.print()


def display_event_detail(event: Event) -> None:
    """Display a single event as a detailed panel."""
    content = f"""
[bold cyan]{event.title}[/bold cyan]

[bold]Description:[/bold] {event.description or "-"}
[bold]Date:[/bold] {event.date_field.strftime("%Y-%m-%d (%A)")}
[bold]Time:[/bold] {format_time(event.time) if event.time else "TBD"}
[bold]Duration:[/bold] {format_duration(event.duration_minutes) if event.duration_minutes else "-"}
[bold]Category:[/bold] {event.category.value.capitalize()}
[bold]Priority:[/bold] {event.priority.value.upper()}
[bold]Status:[/bold] {event.status.value.replace("_", " ").title()}
[bold]ID:[/bold] {event.id}
    """.strip()
    
    panel = Panel(
        content,
        title=f"[bold]Event Details[/bold]",
        border_style=get_priority_style(event.priority),
        padding=(1, 2),
    )
    console.print(panel)


def _format_date_header(event_date: date) -> str:
    """Format date header for display."""
    today = date.today()
    tomorrow = date(today.year, today.month, today.day + 1)
    
    if event_date == today:
        return "[bold]Today[/bold]"
    elif event_date == tomorrow:
        return "[bold]Tomorrow[/bold]"
    return event_date.strftime("%A, %B %d, %Y")
