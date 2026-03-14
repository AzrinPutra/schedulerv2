"""Reminder service for tasks and events."""

from typing import List, Dict, Optional
from datetime import datetime, date, time, timedelta

from .models import Reminder, ReminderType, ReminderConfig
from ..models.schedule import Task, Event
from ..storage import MarkdownStorage
from ..tui.console import console
from ..tui.theme import PRIORITY_COLORS


class ReminderService:
    """Service for managing and sending reminders."""
    
    def __init__(self, storage: MarkdownStorage, config: Optional[ReminderConfig] = None):
        self.storage = storage
        self.config = config or ReminderConfig()
        self._reminders: Dict[str, Reminder] = {}
        self._load_reminders()
    
    def _load_reminders(self) -> None:
        """Load reminders from storage."""
        try:
            all_tasks = self.storage.list_all_tasks()
            for task in all_tasks:
                if task.due_date:
                    reminder = Reminder(
                        task_id=task.id,
                        reminder_type=ReminderType.DUE_DATE,
                        minutes_before=self.config.default_minutes_before,
                    )
                    self._reminders[task.id] = reminder
        except Exception:
            pass
    
    def get_upcoming_task_reminders(self, hours_ahead: int = 24) -> List[tuple]:
        """Get tasks with upcoming due dates.
        
        Returns:
            List of (task, minutes_until_due) tuples
        """
        reminders = []
        now = datetime.now()
        
        for task in self.storage.list_all_tasks():
            if task.due_date and task.status.value != "completed":
                due_datetime = datetime.combine(task.due_date, time(23, 59))
                minutes_until = int((due_datetime - now).total_seconds() / 60)
                
                if 0 < minutes_until <= hours_ahead * 60:
                    reminders.append((task, minutes_until))
        
        return sorted(reminders, key=lambda x: x[1])
    
    def get_upcoming_event_reminders(self, hours_ahead: int = 24) -> List[tuple]:
        """Get events with upcoming start times.
        
        Returns:
            List of (event, minutes_until_start) tuples
        """
        reminders = []
        now = datetime.now()
        
        for event in self.storage.list_all_events():
            if event.date_field and event.time and event.status.value != "completed":
                event_datetime = datetime.combine(event.date_field, event.time)
                minutes_until = int((event_datetime - now).total_seconds() / 60)
                
                if 0 < minutes_until <= hours_ahead * 60:
                    reminders.append((event, minutes_until))
        
        return sorted(reminders, key=lambda x: x[1])
    
    def get_today_tasks(self) -> List[Task]:
        """Get all tasks due today."""
        today = date.today()
        return [
            task for task in self.storage.list_all_tasks()
            if task.due_date == today and task.status.value != "completed"
        ]
    
    def get_today_events(self) -> List[Event]:
        """Get all events for today."""
        today = date.today()
        return [
            event for event in self.storage.list_all_events()
            if event.date_field == today and event.status.value != "completed"
        ]
    
    def send_reminder_notification(self, task: Task, minutes_until: int) -> None:
        """Send a notification for a task reminder."""
        if not self.config.notification_enabled:
            return
        
        if self.config.is_quiet_hours(datetime.now().hour):
            return
        
        priority_style = PRIORITY_COLORS.get(task.priority.value, "white")
        
        if minutes_until < 60:
            time_str = f"{minutes_until} minutes"
        else:
            hours = minutes_until // 60
            time_str = f"{hours} hour{'s' if hours > 1 else ''}"
        
        console.print(f"\n[bold yellow]REMINDER[/bold yellow]")
        console.print(f"[{priority_style}]{task.title}[/{priority_style.split()[0] if priority_style else 'white'}]")
        console.print(f"Due in: {time_str}")
        if task.description:
            console.print(f"[dim]{task.description}[/dim]")
        console.print()
    
    def send_event_notification(self, event: Event, minutes_until: int) -> None:
        """Send a notification for an event reminder."""
        if not self.config.notification_enabled:
            return
        
        if self.config.is_quiet_hours(datetime.now().hour):
            return
        
        priority_style = PRIORITY_COLORS.get(event.priority.value, "white")
        
        if minutes_until < 60:
            time_str = f"{minutes_until} minutes"
        else:
            hours = minutes_until // 60
            time_str = f"{hours} hour{'s' if hours > 1 else ''}"
        
        console.print(f"\n[bold cyan]EVENT REMINDER[/bold cyan]")
        console.print(f"[{priority_style}]{event.title}[/{priority_style.split()[0] if priority_style else 'white'}]")
        console.print(f"Starts in: {time_str}")
        if event.time:
            console.print(f"Time: {event.time.strftime('%H:%M')}")
        console.print()
    
    def print_daily_summary(self) -> None:
        """Print a daily summary of tasks and events."""
        today_tasks = self.get_today_tasks()
        today_events = self.get_today_events()
        
        console.print("\n[bold magenta]=== Today's Schedule ===[/bold magenta]\n")
        
        console.print(f"[bold]Tasks Due Today:[/bold] {len(today_tasks)}")
        for i, task in enumerate(today_tasks, 1):
            priority_style = PRIORITY_COLORS.get(task.priority.value, "white")
            console.print(f"  {i}. [{priority_style}]{task.title}[/{priority_style.split()[0] if priority_style else 'white'}]")
        
        console.print(f"\n[bold]Events Today:[/bold] {len(today_events)}")
        for i, event in enumerate(today_events, 1):
            priority_style = PRIORITY_COLORS.get(event.priority.value, "white")
            time_str = event.time.strftime('%H:%M') if event.time else "TBD"
            console.print(f"  {i}. [{priority_style}]{event.title}[/{priority_style.split()[0] if priority_style else 'white'}] at {time_str}")
        
        console.print()
    
    def check_reminders(self, hours_ahead: int = 24) -> None:
        """Check and send all pending reminders."""
        task_reminders = self.get_upcoming_task_reminders(hours_ahead)
        event_reminders = self.get_upcoming_event_reminders(hours_ahead)
        
        for task, minutes in task_reminders:
            self.send_reminder_notification(task, minutes)
        
        for event, minutes in event_reminders:
            self.send_event_notification(event, minutes)
