# Work Item: Create basic models

**ID**: create-basic-models  
**Intent**: create-schedule-data-models  
**Status**: pending  
**Complexity**: medium  
**Mode**: confirm

## Description

Create the basic data models for the scheduler: Task, Event, ScheduleItem with proper attributes.

## Files to Create

- `src/models/__init__.py` - Package init
- `src/models/schedule.py` - Core schedule models
- `src/models/types.py` - Type definitions

## Requirements

- Use dataclasses for models
- Include proper type hints
- Follow coding standards naming conventions
- Add docstrings for all classes/methods

## Acceptance Criteria

- Task, Event, ScheduleItem classes defined
- Proper attributes included (id, title, date, time, etc.)
- Type hints for all attributes
- Google-style docstrings
