import os
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class StorageConfig:
    root: Path = field(default_factory=lambda: Path.home() / 'scheduler_data')

    @property
    def tasks(self) -> Path:
        return self.root / 'tasks'

    @property
    def events(self) -> Path:
        return self.root / 'events'

    @property
    def schedules(self) -> Path:
        return self.root / 'schedules'

    def ensure_directories(self) -> None:
        for path in [self.tasks, self.events, self.schedules]:
            if not path.exists():
                os.makedirs(path)
