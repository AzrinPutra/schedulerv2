# Work Item: Add CRUD operations

**ID**: add-crud-operations  
**Intent**: create-markdown-storage  
**Status**: pending  
**Complexity**: high  
**Mode**: confirm

## Description

Implement create, read, update, delete operations for tasks and events.

## Files to Modify

- `src/storage/markdown.py` - Add CRUD methods

## Requirements

- `save_task(task)` - Save task to markdown file
- `load_task(task_id)` - Load task from file
- `update_task(task)` - Update existing task
- `delete_task(task_id)` - Delete task file
- Same for events
- `list_tasks()` - List all tasks
- `list_events()` - List all events

## Acceptance Criteria

- All CRUD operations work
- Proper error handling
- Files organized by date
