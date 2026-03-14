import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import date, datetime
from uuid import uuid4
from src.storage import MarkdownStorage, StorageConfig
from src.models import Task, Event, ScheduleItem, Category, Priority, Status


@pytest.fixture
def temp_dir():
    tmp = tempfile.mkdtemp()
    yield Path(tmp)
    shutil.rmtree(tmp)


@pytest.fixture
def storage(temp_dir):
    config = StorageConfig(root=temp_dir)
    config.ensure_directories()
    return MarkdownStorage(config)


def test_save_load_task(storage):
    task_id = str(uuid4())
    task = Task(
        id=task_id,
        title='Test Task 1',
        category=Category.SCHOOL,
        priority=Priority.HIGH,
        status=Status.PENDING,
        due_date=date(2026, 3, 20),
        created_at=datetime(2026, 3, 14, 13, 0, 0),
        updated_at=datetime(2026, 3, 14, 13, 0, 0),
        description='This is a test task.',
    )
    storage.save(task)
    loaded_task = storage.load(task_id)
    assert loaded_task.id == task.id
    assert loaded_task.title == task.title
    assert loaded_task.description == task.description


def test_delete_task(storage):
    task_id = str(uuid4())
    task = Task(
        id=task_id,
        title='Test Task 1',
        category=Category.SCHOOL,
        priority=Priority.HIGH,
        status=Status.PENDING,
        due_date=date(2026, 3, 20),
        created_at=datetime(2026, 3, 14, 13, 0, 0),
        updated_at=datetime(2026, 3, 14, 13, 0, 0),
        description='This is a test task.',
    )
    storage.save(task)
    storage.delete(task_id)
    with pytest.raises(FileNotFoundError):
        storage.load(task_id)


def test_exists_task(storage):
    task_id = str(uuid4())
    task = Task(
        id=task_id,
        title='Test Task 1',
        category=Category.SCHOOL,
        priority=Priority.HIGH,
        status=Status.PENDING,
        due_date=date(2026, 3, 20),
        created_at=datetime(2026, 3, 14, 13, 0, 0),
        updated_at=datetime(2026, 3, 14, 13, 0, 0),
        description='This is a test task.',
    )
    storage.save(task)
    assert storage.exists(task_id) is True
    assert storage.exists('non-existent') is False


def test_list_all_tasks(storage):
    task_ids = [str(uuid4()) for _ in range(3)]
    tasks = [
        Task(
            id=task_ids[i],
            title=f'Test Task {i}',
            category=Category.SCHOOL,
            priority=Priority.HIGH,
            status=Status.PENDING,
            due_date=date(2026, 3, 20),
            created_at=datetime(2026, 3, 14, 13, 0, 0),
            updated_at=datetime(2026, 3, 14, 13, 0, 0),
            description=f'This is a test task {i}.',
        )
        for i in range(3)
    ]
    for task in tasks:
        storage.save(task)
    listed = storage.list_all()
    assert len(listed) >= 3
