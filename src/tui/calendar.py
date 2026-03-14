"""Calendar view for scheduling."""

from typing import List, Set, Dict
from datetime import date, timedelta

from rich.panel import Panel
from rich.text import Text

from ..models.schedule import Event
from .console import console
from .theme import CATEGORY_COLORS


def get_week_dates(ref_date: date = None) -> List[date]:
    """Get the 7 days of the week containing the reference date (Mon-Sun)."""
    if ref_date is None:
        ref_date = date.today()
    
    monday = ref_date - timedelta(days=ref_date.weekday())
    return [monday + timedelta(days=i) for i in range(7)]


def create_week_calendar(
    events_by_date: Dict[date, List[Event]],
    week_start: date = None,
    show_events: bool = True,
) -> Panel:
    """Create a simple week calendar view.
    
    Args:
        events_by_date: Dict mapping dates to list of events
        week_start: The Monday of the week to display
        show_events: Whether to show event names in calendar cells
    
    Returns:
        A Rich Panel containing the week calendar
    """
    if week_start is None:
        week_start = get_week_dates()[0]
    
    week_dates = [week_start + timedelta(days=i) for i in range(7)]
    today = date.today()
    
    lines = []
    
    header_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header_line = "  ".join(
        f"{day:^6}" for day in header_days
    )
    lines.append(f"[bold magenta]{header_line}[/bold magenta]")
    
    date_nums = []
    for d in week_dates:
        if d == today:
            date_nums.append(f"[bold cyan on black]{d.day:^6}[/bold cyan on black]")
        elif d.month != week_start.month:
            date_nums.append(f"[dim]{d.day:^6}[/dim]")
        else:
            date_nums.append(f"{d.day:^6}")
    
    date_line = "  ".join(date_nums)
    lines.append(date_line)
    
    if show_events:
        lines.append("")
        
        max_events = 3
        for i in range(max_events):
            event_line = ""
            for d in week_dates:
                day_events = events_by_date.get(d, [])
                if i < len(day_events):
                    ev = day_events[i]
                    cat_color = CATEGORY_COLORS.get(ev.category.value, "white")
                    ev_name = ev.title[:8] + ".." if len(ev.title) > 10 else ev.title
                    event_line += f"[{cat_color}]{ev_name:^6}[/{cat_color.split()[0] if cat_color else 'white'}]  "
                else:
                    event_line += "       "
            lines.append(event_line)
    
    content = "\n".join(lines)
    
    week_end = week_start + timedelta(days=6)
    title = f"Week of {week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
    
    return Panel(
        content,
        title=title,
        border_style="cyan",
        padding=(1, 2),
    )


def display_week_calendar(
    events_by_date: Dict[date, List[Event]],
    week_start: date = None,
    show_events: bool = True,
) -> None:
    """Display a week calendar view."""
    panel = create_week_calendar(events_by_date, week_start, show_events)
    console.print(panel)
