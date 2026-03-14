# Coding Standards

## Python Style
- Follow PEP 8
- Use 4-space indentation
- Max line length: 88 characters (Black compatible)

## Project Structure
```
src/
├── __init__.py
├── main.py           # Entry point
├── cli.py            # CLI commands
├── scheduler/        # Core logic
│   ├── __init__.py
│   ├── models.py     # Data models
│   ├── storage.py    # SQLite operations
│   └── utils.py      # Helper functions
├── ui/               # TUI components
│   ├── __init__.py
│   ├── views.py
│   └── components.py
└── tests/            # Test files
```

## Naming Conventions
- Classes: `PascalCase` (e.g., `TaskScheduler`)
- Functions/Variables: `snake_case` (e.g., `add_task`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_TASKS_PER_DAY`)

## Type Hints
- Use type hints for all public functions
- Use `from __future__ import annotations` for forward refs

## Error Handling
- Custom exceptions in `scheduler/errors.py`
- User-friendly error messages in TUI

## Documentation
- Docstrings for all public classes/functions (Google style)
- Comments for complex logic only
