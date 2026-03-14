"""Web dashboard for FireSchedule."""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import date, datetime
from typing import Optional

from ..storage import MarkdownStorage
from ..storage.config import StorageConfig
from ..models import Task, Event, Category, Priority, Status

app = FastAPI(
    title="FireSchedule",
    description="Personal Assistant & Weekly Scheduler",
    version="0.1.0",
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

_storage = None


def get_storage() -> MarkdownStorage:
    global _storage
    if _storage is None:
        config = StorageConfig()
        config.ensure_directories()
        _storage = MarkdownStorage(config)
    return _storage


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with today's overview."""
    storage = get_storage()
    
    tasks = storage.list_all_tasks()
    events = storage.list_all_events()
    
    today = date.today()
    today_tasks = [t for t in tasks if t.due_date == today]
    today_events = [e for e in events if e.date_field == today]
    
    upcoming_tasks = [t for t in tasks if t.due_date and t.due_date > today][:5]
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "today": today,
            "today_tasks": today_tasks,
            "today_events": today_events,
            "upcoming_tasks": upcoming_tasks,
            "categories": list(Category),
            "priorities": list(Priority),
        }
    )


@app.get("/tasks", response_class=HTMLResponse)
async def list_tasks(
    request: Request,
    category: Optional[str] = None,
    status: Optional[str] = None,
):
    """List all tasks."""
    storage = get_storage()
    tasks = storage.list_all_tasks()
    
    if category:
        try:
            cat = Category(category.lower())
            tasks = [t for t in tasks if t.category == cat]
        except ValueError:
            pass
    
    if status:
        try:
            stat = Status(status.lower())
            tasks = [t for t in tasks if t.status == stat]
        except ValueError:
            pass
    
    return templates.TemplateResponse(
        "tasks.html",
        {
            "request": request,
            "tasks": tasks,
            "categories": list(Category),
            "statuses": list(Status),
        }
    )


@app.get("/events", response_class=HTMLResponse)
async def list_events(
    request: Request,
    category: Optional[str] = None,
):
    """List all events."""
    storage = get_storage()
    events = storage.list_all_events()
    
    if category:
        try:
            cat = Category(category.lower())
            events = [e for e in events if e.category == cat]
        except ValueError:
            pass
    
    return templates.TemplateResponse(
        "events.html",
        {
            "request": request,
            "events": events,
            "categories": list(Category),
        }
    )


@app.get("/calendar", response_class=HTMLResponse)
async def calendar_view(
    request: Request,
    month: Optional[int] = None,
    year: Optional[int] = None,
):
    """Calendar view."""
    storage = get_storage()
    
    today = date.today()
    if month is None:
        month = today.month
    if year is None:
        year = today.year
    
    tasks = storage.list_all_tasks()
    events = storage.list_all_events()
    
    month_tasks = [t for t in tasks if t.due_date and t.due_date.month == month and t.due_date.year == year]
    month_events = [e for e in events if e.date_field.month == month and e.date_field.year == year]
    
    from calendar import monthrange
    days_in_month = monthrange(year, month)[1]
    
    month_days = []
    for day in range(1, days_in_month + 1):
        day_date = date(year, month, day)
        day_tasks = [t for t in month_tasks if t.due_date == day_date]
        day_events = [e for e in month_events if e.date_field == day_date]
        month_days.append({
            "date": day_date,
            "day": day,
            "tasks": day_tasks,
            "events": day_events,
            "is_today": day_date == today,
        })
    
    from datetime import date as dt_date
    first_day = dt_date(year, month, 1)
    start_padding = first_day.weekday()
    
    month_name = first_day.strftime("%B %Y")
    
    return templates.TemplateResponse(
        "calendar.html",
        {
            "request": request,
            "month_days": month_days,
            "month": month,
            "year": year,
            "month_name": month_name,
            "start_padding": start_padding,
        }
    )


@app.get("/add", response_class=HTMLResponse)
async def add_item(request: Request):
    """Add new task or event page."""
    return templates.TemplateResponse(
        "add.html",
        {
            "request": request,
            "categories": list(Category),
            "priorities": list(Priority),
        }
    )


@app.post("/add/task", response_class=HTMLResponse)
async def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    due_date: str = Form(""),
    category: str = Form("personal"),
    priority: str = Form("medium"),
):
    """Add a new task."""
    storage = get_storage()
    
    due_date_obj = None
    if due_date:
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            pass
    
    try:
        cat = Category(category.lower())
    except ValueError:
        cat = Category.PERSONAL
    
    try:
        pri = Priority(priority.lower())
    except ValueError:
        pri = Priority.MEDIUM
    
    task = Task(
        title=title,
        description=description or None,
        due_date=due_date_obj,
        category=cat,
        priority=pri,
        status=Status.PENDING,
    )
    
    storage.save(task)
    
    return templates.TemplateResponse(
        "add_success.html",
        {
            "request": request,
            "item_type": "Task",
            "item": task,
        }
    )


@app.post("/add/event", response_class=HTMLResponse)
async def add_event(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    date_str: str = Form(""),
    time_str: str = Form(""),
    duration: str = Form("60"),
    category: str = Form("personal"),
    priority: str = Form("medium"),
):
    """Add a new event."""
    storage = get_storage()
    
    event_date = date.today()
    if date_str:
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            pass
    
    event_time = None
    if time_str:
        try:
            event_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            pass
    
    event_duration = 60
    if duration and duration.isdigit():
        event_duration = int(duration)
    
    try:
        cat = Category(category.lower())
    except ValueError:
        cat = Category.PERSONAL
    
    try:
        pri = Priority(priority.lower())
    except ValueError:
        pri = Priority.MEDIUM
    
    event = Event(
        title=title,
        description=description or None,
        date_field=event_date,
        time=event_time,
        duration_minutes=event_duration,
        category=cat,
        priority=pri,
        status=Status.PENDING,
    )
    
    storage.save(event)
    
    return templates.TemplateResponse(
        "add_success.html",
        {
            "request": request,
            "item_type": "Event",
            "item": event,
        }
    )


@app.get("/api/tasks")
async def api_tasks():
    """API endpoint for tasks."""
    storage = get_storage()
    tasks = storage.list_all_tasks()
    return [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "category": t.category.value,
            "priority": t.priority.value,
            "status": t.status.value,
        }
        for t in tasks
    ]


@app.get("/api/events")
async def api_events():
    """API endpoint for events."""
    storage = get_storage()
    events = storage.list_all_events()
    return [
        {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "date": e.date_field.isoformat(),
            "time": e.time.isoformat() if e.time else None,
            "duration": e.duration_minutes,
            "category": e.category.value,
            "priority": e.priority.value,
            "status": e.status.value,
        }
        for e in events
    ]
