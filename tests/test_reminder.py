import pytest
from datetime import date, time, datetime, timedelta
from pathlib import Path
import tempfile
import shutil

from src.models import Task, Event, Category, Priority, Status
from src.storage import MarkdownStorage
from src.storage.config import StorageConfig
from src.reminder.service import ReminderService
from src.reminder.models import ReminderConfig, ReminderType


@pytest.fixture
def temp_storage():
    """Create a temporary storage for testing."""
    temp_dir = tempfile.mkdtemp()
    config = StorageConfig(root=Path(temp_dir))
    config.ensure_directories()
    storage = MarkdownStorage(config)
    yield storage
    shutil.rmtree(temp_dir)


class TestReminderService:
    """Tests for the reminder service."""
    
    def test_get_today_tasks_empty(self, temp_storage):
        """Test getting today's tasks when none exist."""
        service = ReminderService(temp_storage)
        tasks = service.get_today_tasks()
        assert len(tasks) == 0
    
    def test_get_today_tasks_with_due_today(self, temp_storage):
        """Test getting tasks due today."""
        today = date.today()
        task = Task(
            title="Test Task",
            due_date=today,
            status=Status.PENDING
        )
        temp_storage.save(task)
        
        service = ReminderService(temp_storage)
        tasks = service.get_today_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task"
    
    def test_get_today_tasks_excludes_completed(self, temp_storage):
        """Test that completed tasks are excluded."""
        today = date.today()
        task = Task(
            title="Completed Task",
            due_date=today,
            status=Status.COMPLETED
        )
        temp_storage.save(task)
        
        service = ReminderService(temp_storage)
        tasks = service.get_today_tasks()
        assert len(tasks) == 0
    
    def test_get_today_events_empty(self, temp_storage):
        """Test getting today's events when none exist."""
        service = ReminderService(temp_storage)
        events = service.get_today_events()
        assert len(events) == 0
    
    def test_get_today_events_with_today(self, temp_storage):
        """Test getting events for today."""
        today = date.today()
        event = Event(
            title="Test Event",
            date_field=today,
            time=time(10, 0),
            status=Status.PENDING
        )
        temp_storage.save(event)
        
        service = ReminderService(temp_storage)
        events = service.get_today_events()
        assert len(events) == 1
        assert events[0].title == "Test Event"
    
    def test_upcoming_task_reminders(self, temp_storage):
        """Test getting upcoming task reminders."""
        tomorrow = date.today() + timedelta(days=1)
        task = Task(
            title="Future Task",
            due_date=tomorrow,
            status=Status.PENDING
        )
        temp_storage.save(task)
        
        service = ReminderService(temp_storage)
        reminders = service.get_upcoming_task_reminders(hours_ahead=48)
        assert len(reminders) == 1
        assert reminders[0][0].title == "Future Task"
    
    def test_upcoming_event_reminders(self, temp_storage):
        """Test getting upcoming event reminders."""
        tomorrow = date.today() + timedelta(days=1)
        event = Event(
            title="Future Event",
            date_field=tomorrow,
            time=time(14, 0),
            status=Status.PENDING
        )
        temp_storage.save(event)
        
        service = ReminderService(temp_storage)
        reminders = service.get_upcoming_event_reminders(hours_ahead=48)
        assert len(reminders) == 1
        assert reminders[0][0].title == "Future Event"


class TestTaskModel:
    """Tests for Task model."""
    
    def test_create_task(self):
        """Test creating a basic task."""
        task = Task(title="Test Task")
        assert task.title == "Test Task"
        assert task.status == Status.PENDING
        assert task.priority == Priority.MEDIUM
        assert task.category == Category.PERSONAL
    
    def test_task_to_dict(self):
        """Test task serialization."""
        task = Task(title="Test", due_date=date.today())
        data = task.to_dict()
        assert data["title"] == "Test"
        assert "due_date" in data
    
    def test_task_from_dict(self):
        """Test task deserialization."""
        data = {
            "title": "Test Task",
            "due_date": "2024-01-15",
            "category": "school",
            "priority": "high",
            "status": "pending"
        }
        task = Task.from_dict(data)
        assert task.title == "Test Task"
        assert task.category == Category.SCHOOL
        assert task.priority == Priority.HIGH


class TestEventModel:
    """Tests for Event model."""
    
    def test_create_event(self):
        """Test creating a basic event."""
        event = Event(title="Test Event", date_field=date.today())
        assert event.title == "Test Event"
        assert event.date_field == date.today()
    
    def test_event_with_time(self):
        """Test creating event with time."""
        event = Event(
            title="Meeting",
            date_field=date.today(),
            time=time(10, 30),
            duration_minutes=60
        )
        assert event.time == time(10, 30)
        assert event.duration_minutes == 60
    
    def test_event_to_dict(self):
        """Test event serialization."""
        event = Event(title="Test", date_field=date.today())
        data = event.to_dict()
        assert data["title"] == "Test"
        assert "date" in data


class TestStorageIntegration:
    """Integration tests for storage with tasks and events."""
    
    def test_save_and_load_task(self, temp_storage):
        """Test saving and loading a task."""
        task = Task(title="Save Test", due_date=date.today())
        temp_storage.save(task)
        
        loaded = temp_storage.load(task.id)
        assert loaded.title == task.title
        assert loaded.id == task.id
    
    def test_save_and_load_event(self, temp_storage):
        """Test saving and loading an event."""
        event = Event(title="Event Test", date_field=date.today())
        temp_storage.save(event)
        
        loaded = temp_storage.load(event.id)
        assert loaded.title == event.title
    
    def test_delete_task(self, temp_storage):
        """Test deleting a task."""
        task = Task(title="Delete Me")
        temp_storage.save(task)
        
        temp_storage.delete(task.id)
        
        assert not temp_storage.exists(task.id)
    
    def test_list_all_tasks(self, temp_storage):
        """Test listing all tasks."""
        for i in range(3):
            task = Task(title=f"Task {i}", due_date=date.today())
            temp_storage.save(task)
        
        tasks = temp_storage.list_all_tasks()
        assert len(tasks) == 3
    
    def test_list_all_events(self, temp_storage):
        """Test listing all events."""
        for i in range(3):
            event = Event(title=f"Event {i}", date_field=date.today())
            temp_storage.save(event)
        
        events = temp_storage.list_all_events()
        assert len(events) == 3
