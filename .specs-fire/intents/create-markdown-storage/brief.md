# Intent: create-markdown-storage

**ID**: create-markdown-storage  
**Status**: pending  
**Priority**: high  
**Created**: 2026-03-14T13:15:00Z

## Description

Create a markdown-based storage layer for persisting tasks, events, and schedules. Each schedule item will be stored as a markdown file with frontmatter metadata.

## Goals

1. Store each task/event as a markdown file
2. Use YAML frontmatter for metadata (id, dates, category, priority, status)
3. Store description/content in markdown body
4. Organize files by date (year/month structure)
5. Support CRUD operations (create, read, update, delete)
6. Enable git-friendly storage for backup

## Storage Structure

```
data/
├── tasks/
│   ├── 2026/
│   │   └── 03/
│   │       └── task-uuid.md
│   └── ...
├── events/
│   ├── 2026/
│   │   └── 03/
│   │       └── event-uuid.md
│   └── ...
└── schedules/
    └── weekly/
        └── 2026-W11.md
```

## File Format

```markdown
---
id: uuid-here
type: task
title: Task Title
category: school
priority: high
status: pending
due_date: 2026-03-20
created_at: 2026-03-14T13:00:00Z
updated_at: 2026-03-14T13:00:00Z
---

Task description in markdown format.

- Subtask 1
- Subtask 2
```

## Work Items

1. **create-storage-module** (confirm) - Create storage module structure
2. **add-markdown-parser** (confirm) - Add markdown/frontmatter parsing
3. **add-crud-operations** (confirm) - Implement create, read, update, delete
4. **add-date-organization** (autopilot) - Organize files by date

## Dependencies

- pyyaml (for frontmatter parsing)
- Existing models (Task, Event, ScheduleItem)
- Serialization utilities (to_dict/from_dict)

## Acceptance Criteria

- Can save Task/Event to markdown file
- Can load Task/Event from markdown file
- Files organized by date
- Round-trip preserves all data
- Git-friendly (text-based, diffable)
