"""Notion sync service for bi-directional sync with scheduler."""

from typing import Optional, Dict, Any, List
from datetime import date, datetime

from .client import NotionClient, NotionConfig
from ...models import Task, Event, Category, Priority, Status
from ...storage import MarkdownStorage


NOTION_STATUS_MAP = {
    "To Do": Status.PENDING,
    "In Progress": Status.IN_PROGRESS,
    "Done": Status.COMPLETED,
    "Cancelled": Status.CANCELLED,
}

NOTION_PRIORITY_MAP = {
    "Low": Priority.LOW,
    "Medium": Priority.MEDIUM,
    "High": Priority.HIGH,
    "Urgent": Priority.URGENT,
}

NOTION_CATEGORY_MAP = {
    "School": Category.SCHOOL,
    "Learning": Category.LEARNING,
    "Exercise": Category.EXERCISE,
    "Personal": Category.PERSONAL,
    "Work": Category.WORK,
    "Meeting": Category.MEETING,
}


class NotionSync:
    """Sync service between scheduler and Notion."""
    
    def __init__(
        self,
        storage: MarkdownStorage,
        config: Optional[NotionConfig] = None,
    ):
        self.storage = storage
        self.config = config or NotionConfig.from_env()
        self.client = None
        if self.config.is_configured():
            self.client = NotionClient(self.config)
    
    def is_configured(self) -> bool:
        """Check if Notion integration is configured."""
        return self.client is not None
    
    def task_to_notion_properties(self, task: Task) -> Dict[str, Any]:
        """Convert a Task to Notion properties."""
        status_str = next(
            (k for k, v in NOTION_STATUS_MAP.items() if v == task.status),
            "To Do"
        )
        priority_str = next(
            (k for k, v in NOTION_PRIORITY_MAP.items() if v == task.priority),
            "Medium"
        )
        category_str = next(
            (k for k, v in NOTION_CATEGORY_MAP.items() if v == task.category),
            "Personal"
        )
        
        properties = {
            "Name": {
                "title": [{"text": {"content": task.title}}],
            },
            "Status": {
                "select": {"name": status_str},
            },
            "Priority": {
                "select": {"name": priority_str},
            },
            "Category": {
                "select": {"name": category_str},
            },
        }
        
        if task.due_date:
            properties["Due Date"] = {
                "date": {"start": task.due_date.isoformat()},
            }
        
        if task.description:
            properties["Description"] = {
                "rich_text": [{"text": {"content": task.description}}],
            }
        
        return properties
    
    def notion_properties_to_task(self, page: Dict) -> Optional[Task]:
        """Convert Notion page properties to a Task."""
        props = page.get("properties", {})
        
        title = ""
        title_prop = props.get("Name", {})
        if title_prop.get("title"):
            title = title_prop["title"][0].get("plain_text", "")
        
        if not title:
            return None
        
        status = Status.PENDING
        status_prop = props.get("Status", {})
        if status_prop.get("select"):
            status = NOTION_STATUS_MAP.get(
                status_prop["select"].get("name", "To Do"),
                Status.PENDING
            )
        
        priority = Priority.MEDIUM
        priority_prop = props.get("Priority", {})
        if priority_prop.get("select"):
            priority = NOTION_PRIORITY_MAP.get(
                priority_prop["select"].get("name", "Medium"),
                Priority.MEDIUM
            )
        
        category = Category.PERSONAL
        category_prop = props.get("Category", {})
        if category_prop.get("select"):
            category = NOTION_CATEGORY_MAP.get(
                category_prop["select"].get("name", "Personal"),
                Category.PERSONAL
            )
        
        due_date = None
        due_date_prop = props.get("Due Date", {})
        if due_date_prop.get("date") and due_date_prop["date"].get("start"):
            due_date_str = due_date_prop["date"]["start"]
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError:
                pass
        
        description = None
        desc_prop = props.get("Description", {})
        if desc_prop.get("rich_text") and desc_prop["rich_text"]:
            description = desc_prop["rich_text"][0].get("plain_text")
        
        notion_id = page.get("id", "")
        
        return Task(
            id=f"notion_{notion_id}",
            title=title,
            description=description,
            due_date=due_date,
            category=category,
            priority=priority,
            status=status,
        )
    
    def push_task(self, task: Task) -> str:
        """Push a task to Notion. Returns Notion page ID."""
        if not self.client:
            raise RuntimeError("Notion is not configured")
        
        properties = self.task_to_notion_properties(task)
        
        page = self.client.create_page(
            self.config.database_id,
            properties,
        )
        
        return page.get("id", "")
    
    def pull_tasks(self) -> List[Task]:
        """Pull all tasks from Notion database."""
        if not self.client:
            raise RuntimeError("Notion is not configured")
        
        pages = self.client.query_database(self.config.database_id)
        
        tasks = []
        for page in pages:
            task = self.notion_properties_to_task(page)
            if task:
                tasks.append(task)
        
        return tasks
    
    def sync_to_notion(self) -> Dict[str, int]:
        """Sync all local tasks to Notion. Returns stats."""
        if not self.client:
            raise RuntimeError("Notion is not configured")
        
        local_tasks = self.storage.list_all_tasks()
        pushed = 0
        
        for task in local_tasks:
            try:
                self.push_task(task)
                pushed += 1
            except Exception:
                pass
        
        return {"pushed": pushed}
    
    def sync_from_notion(self) -> Dict[str, int]:
        """Sync tasks from Notion to local storage. Returns stats."""
        if not self.client:
            raise RuntimeError("Notion is not configured")
        
        notion_tasks = self.pull_tasks()
        imported = 0
        
        for task in notion_tasks:
            task.id = task.id.replace("notion_", "")
            self.storage.save(task)
            imported += 1
        
        return {"imported": imported}
    
    def full_sync(self) -> Dict[str, int]:
        """Perform full bi-directional sync."""
        from_notion = self.sync_from_notion()
        to_notion = self.sync_to_notion()
        
        return {
            "imported": from_notion.get("imported", 0),
            "pushed": to_notion.get("pushed", 0),
        }
