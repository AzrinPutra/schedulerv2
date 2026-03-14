import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from datetime import datetime, date, time, timedelta
from pathlib import Path

from .models import Task, Event, Category, Priority, Status
from .models.schedule import ScheduleItem
from .storage import MarkdownStorage
from .storage.config import StorageConfig
from .tui.task_display import display_tasks, display_task_detail
from .tui.event_display import display_events
from .tui.calendar import display_week_calendar
from .tui.theme import PRIORITY_COLORS, CATEGORY_COLORS, STATUS_COLORS
from .reminder.service import ReminderService
from .reminder.models import ReminderConfig
from .git.automation import GitAutomation
from .git.export import ScheduleExporter

console = Console()

app = typer.Typer(
    name="scheduler",
    help="FireSchedule - Personal Assistant & Weekly Scheduler",
    add_completion=False,
)

_storage = None
_reminder_service = None
_git_automation = None
_exporter = None


def get_storage() -> MarkdownStorage:
    global _storage
    if _storage is None:
        config = StorageConfig()
        config.ensure_directories()
        _storage = MarkdownStorage(config)
    return _storage


def get_reminder_service() -> ReminderService:
    global _reminder_service
    if _reminder_service is None:
        _reminder_service = ReminderService(get_storage())
    return _reminder_service


def get_git_automation() -> GitAutomation:
    global _git_automation
    if _git_automation is None:
        _git_automation = GitAutomation()
    return _git_automation


def get_exporter() -> ScheduleExporter:
    global _exporter
    if _exporter is None:
        _exporter = ScheduleExporter(get_storage())
    return _exporter


@app.command()
def version():
    """Show the version of FireSchedule."""
    from . import __version__
    console.print(f"[green]FireSchedule v{__version__}[/green]")


@app.command()
def add():
    """Add a new task or event."""
    console.print("[bold]Add New Item[/bold]\n")
    
    item_type = Prompt.ask(
        "What would you like to add?",
        choices=["task", "event"],
        default="task"
    )
    
    storage = get_storage()
    
    if item_type == "task":
        title = Prompt.ask("Task title")
        description = Prompt.ask("Description (optional)", default="")
        due_date_str = Prompt.ask("Due date (YYYY-MM-DD, optional)", default="")
        
        console.print("\n[bold]Category:[/bold]")
        categories = list(Category)
        for i, cat in enumerate(categories, 1):
            console.print(f"  {i}. {cat.value}")
        cat_choice = Prompt.ask("Choose category", default="1")
        category = categories[int(cat_choice) - 1] if cat_choice.isdigit() and int(cat_choice) <= len(categories) else Category.PERSONAL
        
        console.print("\n[bold]Priority:[/bold]")
        priorities = list(Priority)
        for i, pri in enumerate(priorities, 1):
            console.print(f"  {i}. {pri.value}")
        pri_choice = Prompt.ask("Choose priority", default="2")
        priority = priorities[int(pri_choice) - 1] if pri_choice.isdigit() and int(pri_choice) <= len(priorities) else Priority.MEDIUM
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError:
                console.print("[red]Invalid date format, ignoring.[/red]")
        
        task = Task(
            title=title,
            description=description or None,
            due_date=due_date,
            category=category,
            priority=priority,
            status=Status.PENDING,
        )
        
        storage.save(task)
        console.print(f"\n[green]Task added successfully![/green]")
        console.print(f"ID: {task.id}")
        
    else:
        title = Prompt.ask("Event title")
        description = Prompt.ask("Description (optional)", default="")
        date_str = Prompt.ask("Date (YYYY-MM-DD)", default=date.today().strftime("%Y-%m-%d"))
        time_str = Prompt.ask("Time (HH:MM, optional)", default="")
        duration = Prompt.ask("Duration in minutes (optional)", default="")
        
        console.print("\n[bold]Category:[/bold]")
        categories = list(Category)
        for i, cat in enumerate(categories, 1):
            console.print(f"  {i}. {cat.value}")
        cat_choice = Prompt.ask("Choose category", default="1")
        category = categories[int(cat_choice) - 1] if cat_choice.isdigit() and int(cat_choice) <= len(categories) else Category.PERSONAL
        
        console.print("\n[bold]Priority:[/bold]")
        priorities = list(Priority)
        for i, pri in enumerate(priorities, 1):
            console.print(f"  {i}. {pri.value}")
        pri_choice = Prompt.ask("Choose priority", default="2")
        priority = priorities[int(pri_choice) - 1] if pri_choice.isdigit() and int(pri_choice) <= len(priorities) else Priority.MEDIUM
        
        event_date = None
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            console.print("[red]Invalid date format, using today.[/red]")
            event_date = date.today()
        
        event_time = None
        if time_str:
            try:
                event_time = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                console.print("[red]Invalid time format, ignoring.[/red]")
        
        event_duration = None
        if duration and duration.isdigit():
            event_duration = int(duration)
        
        event = Event(
            title=title,
            description=description or None,
            date_field=event_date,
            time=event_time,
            duration_minutes=event_duration,
            category=category,
            priority=priority,
            status=Status.PENDING,
        )
        
        storage.save(event)
        console.print(f"\n[green]Event added successfully![/green]")
        console.print(f"ID: {event.id}")


@app.command()
def list(
    item_type: str = typer.Option("all", "--type", "-t", help="Filter by type: task, event, or all"),
    category: str = typer.Option(None, "--category", "-c", help="Filter by category"),
    status: str = typer.Option(None, "--status", "-s", help="Filter by status"),
):
    """List all scheduled tasks and events."""
    storage = get_storage()
    
    tasks = storage.list_all_tasks()
    events = storage.list_all_events()
    
    if category:
        try:
            cat = Category(category.lower())
            tasks = [t for t in tasks if t.category == cat]
            events = [e for e in events if e.category == cat]
        except ValueError:
            console.print(f"[red]Invalid category: {category}[/red]")
            return
    
    if status:
        try:
            stat = Status(status.lower())
            tasks = [t for t in tasks if t.status == stat]
            events = [e for e in events if e.status == stat]
        except ValueError:
            console.print(f"[red]Invalid status: {status}[/red]")
            return
    
    if item_type == "task" or item_type == "all":
        if tasks:
            display_tasks(tasks)
        else:
            console.print("[dim]No tasks found.[/dim]")
    
    if item_type == "event" or item_type == "all":
        if events:
            display_events(events)
        else:
            console.print("[dim]No events found.[/dim]")
    
    if not tasks and not events:
        console.print("[dim]No items found.[/dim]")


@app.command()
def today():
    """Show today's schedule."""
    reminder_service = get_reminder_service()
    reminder_service.print_daily_summary()


@app.command()
def week(
    start_date: str = typer.Option(None, "--start", "-s", help="Start date (YYYY-MM-DD)")
):
    """Show this week's calendar."""
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError:
            console.print("[red]Invalid date format, using today.[/red]")
            start = date.today()
    else:
        start = date.today()
    
    storage = get_storage()
    events = storage.list_all_events()
    
    from collections import defaultdict
    events_by_date = defaultdict(list)
    for event in events:
        events_by_date[event.date_field].append(event)
    
    display_week_calendar(dict(events_by_date), start, True)


@app.command()
def reminder(
    hours: int = typer.Option(24, "--hours", "-h", help="Check hours ahead"),
    summary: bool = typer.Option(False, "--summary", "-s", help="Show daily summary"),
):
    """Check and display reminders."""
    reminder_service = get_reminder_service()
    
    if summary:
        reminder_service.print_daily_summary()
    else:
        reminder_service.check_reminders(hours)
        console.print("[dim]No pending reminders.[/dim]")


@app.command()
def complete(
    item_id: str = typer.Argument(..., help="Task or Event ID to mark complete"),
):
    """Mark a task or event as completed."""
    storage = get_storage()
    
    try:
        item = storage.load(item_id)
        if hasattr(item, 'status'):
            item.status = Status.COMPLETED
            storage.save(item)
            console.print(f"[green]Marked '{item.title}' as completed.[/green]")
        else:
            console.print("[red]Item does not have status field.[/red]")
    except FileNotFoundError:
        console.print(f"[red]Item not found: {item_id}[/red]")


@app.command()
def delete(
    item_id: str = typer.Argument(..., help="Task or Event ID to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a task or event."""
    storage = get_storage()
    
    if not force:
        if not Confirm.ask(f"Delete item '{item_id}'?"):
            console.print("[yellow]Cancelled.[/yellow]")
            return
    
    try:
        storage.delete(item_id)
        console.print(f"[green]Deleted item: {item_id}[/green]")
    except FileNotFoundError:
        console.print(f"[red]Item not found: {item_id}[/red]")


@app.command()
def export(
    export_type: str = typer.Argument(..., help="Export type: daily, weekly"),
    date_str: str = typer.Option(None, "--date", "-d", help="Date for daily (YYYY-MM-DD), start date for weekly"),
    output: str = typer.Option(None, "--output", "-o", help="Output file path"),
):
    """Export schedule to markdown file."""
    exporter = get_exporter()
    
    if export_type == "daily":
        if date_str:
            try:
                export_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                console.print("[red]Invalid date format, using today.[/red]")
                export_date = date.today()
        else:
            export_date = date.today()
        
        content = exporter.export_daily_schedule(export_date)
        
    elif export_type == "weekly":
        if date_str:
            try:
                start = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                console.print("[red]Invalid date format, using today.[/red]")
                start = date.today()
        else:
            start = date.today()
        
        content = exporter.export_weekly_schedule(start)
    
    else:
        console.print(f"[red]Unknown export type: {export_type}[/red]")
        return
    
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
        console.print(f"[green]Exported to: {output}[/green]")
    else:
        console.print(content)


@app.command()
def backup(
    message: str = typer.Option(None, "--message", "-m", help="Commit message"),
    push: bool = typer.Option(True, "--push/--no-push", help="Push to remote after backup"),
):
    """Backup schedule to Git."""
    git = get_git_automation()
    
    if not message:
        message = f"Backup: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    try:
        git.add()
        git.commit(message)
        console.print("[green]Changes committed.[/green]")
        
        if push:
            result = git.push()
            if result:
                console.print("[green]Pushed to remote.[/green]")
            else:
                console.print("[yellow]Push skipped (no remote or no changes).[/yellow]")
        else:
            console.print("[yellow]Skipped push.[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Backup failed: {e}[/red]")


@app.command()
def settings():
    """Configure FireSchedule."""
    console.print("[bold]Settings[/bold]\n")
    
    config = StorageConfig()
    console.print(f"Data directory: {config.root}")
    
    console.print("\n[bold]Categories:[/bold]")
    for cat in Category:
        console.print(f"  - {cat.value}")
    
    console.print("\n[bold]Priorities:[/bold]")
    for pri in Priority:
        console.print(f"  - {pri.value}")
    
    console.print("\n[bold]Statuses:[/bold]")
    for stat in Status:
        console.print(f"  - {stat.value}")


@app.command()
def server(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
):
    """Start the web dashboard server."""
    import uvicorn
    from .web import app as web_app
    
    console.print(f"[green]Starting web server at http://{host}:{port}[/green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]")
    
    uvicorn.run(
        "src.web.app:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    app()
