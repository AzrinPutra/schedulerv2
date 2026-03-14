"""Schedule export to markdown."""

from pathlib import Path
from typing import List, Optional
from datetime import date, datetime, timedelta
from collections import defaultdict

from ..models.schedule import Task, Event
from ..models.enums import Priority, Status
from ..storage import MarkdownStorage


class ScheduleExporter:
    """Export schedule data to markdown files."""
    
    def __init__(self, storage: MarkdownStorage, output_dir: Path = None):
        self.storage = storage
        self.output_dir = output_dir or Path.cwd() / "exports"
    
    def export_task(self, task: Task) -> str:
        """Export a single task to markdown."""
        lines = [
            f"# {task.title}",
            "",
            f"**ID:** {task.id}",
            f"**Created:** {task.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"**Updated:** {task.updated_at.strftime('%Y-%m-%d %H:%M')}",
            "",
        ]
        
        if task.description:
            lines.append(f"**Description:** {task.description}")
            lines.append("")
        
        lines.extend([
            f"**Due Date:** {task.due_date.strftime('%Y-%m-%d') if task.due_date else 'Not set'}",
            f"**Category:** {task.category.value.capitalize()}",
            f"**Priority:** {task.priority.value.upper()}",
            f"**Status:** {task.status.value.replace('_', ' ').title()}",
            "",
        ])
        
        return "\n".join(lines)
    
    def export_event(self, event: Event) -> str:
        """Export a single event to markdown."""
        lines = [
            f"# {event.title}",
            "",
            f"**ID:** {event.id}",
            f"**Created:** {event.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"**Updated:** {event.updated_at.strftime('%Y-%m-%d %H:%M')}",
            "",
        ]
        
        if event.description:
            lines.append(f"**Description:** {event.description}")
            lines.append("")
        
        lines.extend([
            f"**Date:** {event.date_field.strftime('%Y-%m-%d')}",
            f"**Time:** {event.time.strftime('%H:%M') if event.time else 'TBD'}",
            f"**Duration:** {event.duration_minutes} minutes" if event.duration_minutes else "**Duration:** Not set",
            f"**Category:** {event.category.value.capitalize()}",
            f"**Priority:** {event.priority.value.upper()}",
            f"**Status:** {event.status.value.replace('_', ' ').title()}",
            "",
        ])
        
        return "\n".join(lines)
    
    def export_daily_schedule(self, export_date: date = None) -> str:
        """Export daily schedule to markdown."""
        if export_date is None:
            export_date = date.today()
        
        tasks = [
            t for t in self.storage.list_all_tasks()
            if t.due_date == export_date
        ]
        
        events = [
            e for e in self.storage.list_all_events()
            if e.date_field == export_date
        ]
        
        lines = [
            f"# Daily Schedule - {export_date.strftime('%A, %B %d, %Y')}",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Tasks",
            "",
        ]
        
        if tasks:
            for task in sorted(tasks, key=lambda t: t.priority.value):
                priority_emoji = {
                    Priority.URGENT: "🔴",
                    Priority.HIGH: "🟠",
                    Priority.MEDIUM: "🟡",
                    Priority.LOW: "🟢",
                }.get(task.priority, "⚪")
                
                status_checkbox = "[x]" if task.status == Status.COMPLETED else "[ ]"
                
                lines.append(f"- {priority_emoji} {status_checkbox} **{task.title}**")
                if task.description:
                    lines.append(f"  - {task.description}")
                lines.append(f"  - Category: {task.category.value} | Priority: {task.priority.value}")
                lines.append("")
        else:
            lines.append("*No tasks for this day.*")
            lines.append("")
        
        lines.extend([
            "## Events",
            "",
        ])
        
        if events:
            sorted_events = sorted(events, key=lambda e: e.time or datetime.min.time())
            for event in sorted_events:
                time_str = event.time.strftime('%H:%M') if event.time else "TBD"
                lines.append(f"### {time_str} - {event.title}")
                lines.append("")
                if event.description:
                    lines.append(f"_{event.description}_")
                    lines.append("")
                lines.append(f"- Duration: {event.duration_minutes} min" if event.duration_minutes else "- Duration: TBD")
                lines.append(f"- Category: {event.category.value}")
                lines.append(f"- Priority: {event.priority.value}")
                lines.append("")
        else:
            lines.append("*No events for this day.*")
            lines.append("")
        
        return "\n".join(lines)
    
    def export_weekly_schedule(self, week_start: date = None) -> str:
        """Export weekly schedule to markdown."""
        if week_start is None:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
        
        week_end = week_start + timedelta(days=6)
        
        lines = [
            f"# Weekly Schedule",
            f"## {week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
        ]
        
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_tasks = [t for t in self.storage.list_all_tasks() if t.due_date == day]
            day_events = [e for e in self.storage.list_all_events() if e.date_field == day]
            
            day_name = day.strftime('%A')
            is_today = day == date.today()
            
            header = f"## {day_name}, {day.strftime('%B %d')}"
            if is_today:
                header += " *(Today)*"
            
            lines.append(header)
            lines.append("")
            
            if day_tasks or day_events:
                if day_tasks:
                    lines.append("**Tasks:**")
                    for task in day_tasks:
                        status = "✅" if task.status == Status.COMPLETED else "⬜"
                        lines.append(f"- {status} {task.title}")
                    lines.append("")
                
                if day_events:
                    lines.append("**Events:**")
                    for event in sorted(day_events, key=lambda e: e.time or datetime.min.time()):
                        time_str = event.time.strftime('%H:%M') if event.time else "TBD"
                        lines.append(f"- {time_str}: {event.title}")
                    lines.append("")
            else:
                lines.append("*Nothing scheduled.*")
                lines.append("")
        
        return "\n".join(lines)
    
    def export_all_tasks(self) -> str:
        """Export all tasks to markdown."""
        tasks = self.storage.list_all_tasks()
        
        by_status = defaultdict(list)
        for task in tasks:
            by_status[task.status].append(task)
        
        lines = [
            "# All Tasks",
            "",
            f"**Total:** {len(tasks)}",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
        ]
        
        for status in [Status.PENDING, Status.IN_PROGRESS, Status.COMPLETED, Status.CANCELLED]:
            status_tasks = by_status.get(status, [])
            if status_tasks:
                lines.append(f"## {status.value.replace('_', ' ').title()} ({len(status_tasks)})")
                lines.append("")
                for task in sorted(status_tasks, key=lambda t: t.due_date or date.max):
                    lines.append(f"- **{task.title}**")
                    if task.due_date:
                        lines.append(f"  - Due: {task.due_date.strftime('%Y-%m-%d')}")
                    lines.append(f"  - Category: {task.category.value} | Priority: {task.priority.value}")
                    lines.append("")
        
        return "\n".join(lines)
    
    def save_to_file(self, content: str, filename: str) -> Path:
        """Save markdown content to file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.output_dir / filename
        filepath.write_text(content)
        return filepath
