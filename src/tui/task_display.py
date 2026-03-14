"""Task display using Rich Table."""

from typing import List, Optional
from datetime import date

from rich.table import Table
from rich.text import Text
from rich.panel import Panel

from ..models.schedule import Task
from ..models.enums import Priority, Status, Category
from .console import console
from .theme import PRIORITY_COLORS, STATUS_COLORS, CATEGORY_COLORS


def get_priority_style(priority: Priority) -> str:
    """Get Rich style string for priority."""
    return PRIORITY_COLORS.get(priority.value, "white")


def get_status_style(status: Status) -> str:
    """Get Rich style string for status."""
    return STATUS_COLORS.get(status.value, "white")


def get_category_style(category: Category) -> str:
    """Get Rich style string for category."""
    return CATEGORY_COLORS.get(category.value, "white")


def format_due_date(due_date: Optional[date]) -> str:
    """Format due date for display."""
    if due_date is None:
        return "-"
    today = date.today()
    if due_date == today:
        return "[bold]Today[/bold]"
    elif due_date == today.__class__(today.year, today.month, today.day + 1):
        return "[bold]Tomorrow[/bold]"
    return due_date.strftime("%Y-%m-%d")


def create_task_table(tasks: List[Task], title: str = "Tasks") -> Table:
    """Create a Rich Table displaying tasks with color-coded priorities."""
    table = Table(
        title=title,
        show_header=True,
        header_style="bold magenta",
        expand=True,
        box=None,
    )

    table.add_column("Priority", width=10, justify="center")
    table.add_column("Title", style="cyan", min_width=20)
    table.add_column("Due Date", width=12, justify="center")
    table.add_column("Category", width=12, justify="center")
    table.add_column("Status", width=12, justify="center")

    sorted_tasks = sorted(
        tasks,
        key=lambda t: (
            Priority.URGENT.value if t.priority == Priority.URGENT else
            Priority.HIGH.value if t.priority == Priority.HIGH else
            Priority.MEDIUM.value if t.priority == Priority.MEDIUM else
            Priority.LOW.value
        )
    )

    for task in sorted_tasks:
        priority_text = Text(
            task.priority.value.upper(),
            style=get_priority_style(task.priority)
        )
        
        title_text = Text(task.title)
        if task.description:
            title_text.append(f"\n[dim]{task.description[:50]}...", style="dim")
        
        due_date_text = Text(
            format_due_date(task.due_date),
            style="bold" if task.due_date == date.today() else ""
        )
        
        category_text = Text(
            task.category.value.capitalize(),
            style=get_category_style(task.category)
        )
        
        status_text = Text(
            task.status.value.replace("_", " ").title(),
            style=get_status_style(task.status)
        )
        
        table.add_row(
            priority_text,
            title_text,
            due_date_text,
            category_text,
            status_text,
        )

    return table


def display_tasks(tasks: List[Task], title: str = "Tasks") -> None:
    """Display tasks in a formatted table."""
    if not tasks:
        console.print("[dim]No tasks to display[/dim]")
        return
    
    table = create_task_table(tasks, title)
    console.print(table)


def display_task_detail(task: Task) -> None:
    """Display a single task as a detailed panel."""
    from rich.style import Style
    
    category_style = get_category_style(task.category)
    priority_style = get_priority_style(task.priority)
    status_style = get_status_style(task.status)
    
    content = f"""
[bold cyan]{task.title}[/bold cyan]

[bold]Description:[/bold] {task.description or "-"}
[bold]Due Date:[/bold] {format_due_date(task.due_date)}
[bold]Category:[/bold] {task.category.value.capitalize()}
[bold]Priority:[/bold] {task.priority.value.upper()}
[bold]Status:[/bold] {task.status.value.replace("_", " ").title()}
[bold]ID:[/bold] {task.id}
    """.strip()
    
    panel = Panel(
        content,
        title=f"[bold]Task Details[/bold]",
        border_style=priority_style,
        padding=(1, 2),
    )
    console.print(panel)
