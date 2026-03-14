# System Architecture

## Overview
A personal assistant/scheduler with TUI for managing weekly/daily tasks. Schedule output as Markdown for version control.

## Components

### Core Layer (`src/scheduler/`)
- Task management (add, view, update, delete)
- Schedule calendar (daily/weekly view)
- Reminder system
- User configuration
- Markdown output generator

### UI Layer (`src/ui/`)
- TUI components using Rich
- Interactive prompts (questionary/Inquirer.py)
- Calendar visualization
- Markdown file viewer

### Output Layer (`src/output/`)
- Markdown file generation
- Weekly schedule formatting
- Daily overview templates

### Storage Layer
- Markdown files as source of truth (backed up to git)
- SQLite optional for performance (can be regenerated from Markdown)

### CLI Layer (`src/cli.py`)
- Entry point via `scheduler` command
- Commands: `add`, `list`, `remind`, `setup`, `push`

## Data Flow
```
User Input → CLI → Scheduler Core → Markdown Output → Git Commit → GitHub
                              → [Optional: SQLite for fast access]
                              → UI Display
```

## Markdown Format
```
# Weekly Schedule (Week X)
## Day
- Task 1
- Task 2

## Resources/Learning
- Python: Topic X
- Bash: Topic Y
```

## Future Extensibility
- Plugin system for future features
- External calendar sync (future)
- Notifications (future)
- Git auto-commit/push after changes
