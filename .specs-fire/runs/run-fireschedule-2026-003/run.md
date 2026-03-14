# Run: add-validation

**ID**: run-fireschedule-2026-003  
**Start**: 2026-03-14T12:55:00Z  
**Scope**: single  
**Mode**: confirm  
**Work Item**: add-validation

## Files Changed

| File | Action | Purpose |
|------|--------|---------|
| `src/models/validation.py` | Created | Validation utility functions |
| `src/models/schedule.py` | Modified | Added validation to models |
| `src/models/__init__.py` | Modified | Added validation exports |

## Decisions

- Created standalone validation module for reusability
- Used Pydantic ValidationError for consistency
- Added validation to __post_init__ methods
- Created custom validation exceptions

## Test Results

N/A (no tests yet for basic structure)
