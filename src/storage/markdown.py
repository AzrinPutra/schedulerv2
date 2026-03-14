import os
from pathlib import Path
from typing import Generic, Any, Union, Type
import yaml
from .base import StorageBase
from ..models import Task, Event, ScheduleItem
from .config import StorageConfig
from datetime import datetime, date


class MarkdownStorage(StorageBase):
    def __init__(self, config: StorageConfig) -> None:
        super().__init__()
        self.config = config

    def _get_base_path(self, item_type: str) -> Path:
        paths = {
            'task': self.config.tasks,
            'event': self.config.events,
            'schedule': self.config.schedules,
        }
        return paths[item_type]

    def _get_date_from_item(self, item: Union[Task, Event, ScheduleItem]) -> date:
        if isinstance(item, Task) and item.due_date:
            return item.due_date
        elif hasattr(item, 'date_field') and item.date_field:
            return item.date_field
        return date.today()

    def _get_path(self, item: Union[Task, Event, ScheduleItem], item_type: str, id: str) -> Path:
        item_date = self._get_date_from_item(item)
        base_path = self._get_base_path(item_type)
        year_month = f'{item_date.year}/{item_date.month:02d}'
        return base_path / year_month / f'{id}.md'

    def _write_to_file(self, path: Path, frontmatter: dict, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(yaml.dump(frontmatter, default_flow_style=False))
            f.write('---\n')
            f.write(content or '')

    def _read_from_file(self, path: Path) -> tuple[dict, str]:
        with open(path, 'r') as f:
            content = f.read()
            if '\n---\n' in content:
                frontmatter, *content_lines = content.split('\n---\n')
                return yaml.safe_load(frontmatter), '\n'.join(content_lines or [])
            return {}, content
        return yaml.safe_load(''), ''

    def _search_paths(self, item_type: str, id: str) -> list[Path]:
        base_path = self._get_base_path(item_type)
        if not base_path.exists():
            return []
        paths = []
        for year_dir in base_path.iterdir():
            if year_dir.is_dir():
                for month_dir in year_dir.iterdir():
                    if month_dir.is_dir():
                        file_path = month_dir / f'{id}.md'
                        if file_path.exists():
                            paths.append(file_path)
        return paths

    def save(self, item: Union[Task, Event, ScheduleItem]) -> None:
        item_type = item.__class__.__name__.lower()
        id_ = item.id
        path = self._get_path(item, item_type, id_)
        frontmatter = item.to_dict()
        self._write_to_file(path, frontmatter, item.description or '')

    def load(self, id: str) -> Union[Task, Event, ScheduleItem]:
        model_map = {'task': Task, 'event': Event, 'schedule': ScheduleItem}
        for item_type, model in model_map.items():
            paths = self._search_paths(item_type, id)
            if paths:
                frontmatter, content = self._read_from_file(paths[0])
                return model.from_dict(frontmatter)
        raise FileNotFoundError(f'No item found with id {id}')

    def delete(self, id: str) -> None:
        model_map = {'task': Task, 'event': Event, 'schedule': ScheduleItem}
        for item_type, _ in model_map.items():
            paths = self._search_paths(item_type, id)
            if paths:
                os.remove(paths[0])
                return
        raise FileNotFoundError(f'No item found with id {id}')

    def exists(self, id: str) -> bool:
        model_map = {'task': Task, 'event': Event, 'schedule': ScheduleItem}
        for item_type, _ in model_map.items():
            paths = self._search_paths(item_type, id)
            if paths:
                return True
        return False

    def list_all(self) -> list:
        items = []
        model_map = {'task': Task, 'event': Event, 'schedule': ScheduleItem}
        for item_type, _ in model_map.items():
            base_path = self._get_base_path(item_type)
            if base_path.exists():
                for year_dir in base_path.iterdir():
                    if year_dir.is_dir():
                        for month_dir in year_dir.iterdir():
                            if month_dir.is_dir():
                                for file in month_dir.glob('*.md'):
                                    frontmatter, _ = self._read_from_file(file)
                                    if frontmatter:
                                        items.append(frontmatter)
        return items

    @staticmethod
    def generate_id(item: Union[Task, Event, ScheduleItem]) -> str:
        return f'{item.__class__.__name__.lower()}_{datetime.now().isoformat()}'
