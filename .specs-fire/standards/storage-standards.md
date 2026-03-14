# Storage Standards

## Markdown Files (Source of Truth)

### Location: `schedules/`
```
schedules/
├── weekly/           # Weekly schedule files
│   └── week-01-2026.md
├── daily/            # Daily overviews (generated on request)
│   └── day-2026-03-15.md
└── templates/        # Markdown templates
    ├── weekly-template.md
    └── daily-template.md
```

### Format
- Markdown files are human-readable and git-friendly
- Use clear section headers for days
- Include task status (✅ completed, ⏳ pending, 🔴 missed)
- Link to learning resources

### Backup Strategy
- All Markdown files committed to git
- GitHub as remote backup
- Auto-commit after changes (configurable)

## SQLite (Optional, Cached View)

### Location: `data/scheduler.db`

### Purpose
- Fast local queries (reminders, lookup)
- Can be regenerated from Markdown files
- Not the source of truth

### Tables
```sql
tasks (id, title, description, day, status, created_at)
schedule (id, week_number, date_range, markdown_path)
users (id, name, timezone, preferences)
```

### Sync Strategy
- Markdown → SQLite: Read-only from SQLite when available
- SQLite → Markdown: Never ( Markdown is source of truth)