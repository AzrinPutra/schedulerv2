# Testing Standards

## Test Structure
```
tests/
├── __init__.py
├── test_models.py
├── test_storage.py
├── test_cli.py
└── test_ui.py
```

## Test Patterns
- Unit tests for pure functions
- Integration tests for SQLite operations
- Mock external dependencies (if any)

## Coverage
- Minimum 80% coverage
- pytest-cov for coverage reporting

## Running Tests
```bash
pytest
pytest --cov=scheduler --cov-report=term-missing
```
