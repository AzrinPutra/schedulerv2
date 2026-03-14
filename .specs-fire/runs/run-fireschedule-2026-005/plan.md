# Plan: run-fireschedule-2026-005

**Intent**: create-markdown-storage  
**Work Item**: create-storage-module  
**Mode**: confirm

## Objective

Create the storage module structure with base classes and configuration for markdown-based persistence.

## Files to Create

1. **`src/storage/__init__.py`** - Package initialization with exports
2. **`src/storage/config.py`** - StorageConfig dataclass for path configuration
3. **`src/storage/base.py`** - Abstract base class defining storage interface
4. **`src/storage/markdown.py`** - MarkdownStorage implementation

## Implementation Details

### StorageConfig (config.py)
- Dataclass with storage root path
- Properties for tasks/, events/, schedules/ subdirectories
- Method to ensure directories exist

### StorageBase (base.py)
- Abstract base class with ABCMeta
- Abstract methods: save(), load(), delete(), exists(), list_all()
- Common utility methods for ID generation

### MarkdownStorage (markdown.py)
- Inherits from StorageBase
- Uses pyyaml for frontmatter parsing
- Implements all CRUD operations
- Integrates with existing serialization (to_dict/from_dict)

## Dependencies

- Add `pyyaml>=6.0` to requirements.txt
- Import existing models (Task, Event, ScheduleItem)
- Use serialization utilities from src/models/serialization.py

## Acceptance Criteria

- [ ] Storage module structure created
- [ ] StorageConfig class with path management
- [ ] StorageBase abstract class with interface
- [ ] MarkdownStorage skeleton implemented
- [ ] pyyaml added to requirements.txt
- [ ] No circular imports
- [ ] Type hints throughout
