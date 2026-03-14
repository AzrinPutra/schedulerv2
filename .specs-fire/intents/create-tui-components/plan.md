# Plan: create-tui-components

## Intent Overview
Create TUI components using Rich library for displaying tasks and events in an aesthetically pleasing interface.

## Data Models
- **Task**: id, title, description, due_date, category, priority, status
- **Event**: id, title, description, date_field, category, priority, status, time, duration_minutes

## Priority Colors (Rich)
- URGENT: red bold
- HIGH: magenta
- MEDIUM: yellow
- LOW: green

## Status Colors (Rich)
- PENDING: yellow
- IN_PROGRESS: cyan
- COMPLETED: green bold
- CANCELLED: dim red

## Category Colors (Rich)
- SCHOOL: blue
- LEARNING: magenta
- EXERCISE: green
- PERSONAL: cyan
- WORK: white
- MEETING: yellow

## Work Items

### 1. create-tui-base
**Files to create:**
- `src/tui/__init__.py` - Package exports
- `src/tui/theme.py` - Color scheme and theme constants
- `src/tui/console.py` - Console singleton with theme

**Implementation:**
- Create Rich Console with custom theme
- Define color constants for priorities, statuses, categories
- Create base Panel styles

### 2. add-task-list-display
**Files to create/modify:**
- `src/tui/task_display.py` - TaskListDisplay class

**Implementation:**
- Rich Table with columns: Priority, Title, Due Date, Category, Status
- Color-coded rows based on priority
- Status badges with colors
- Sort by priority (URGENT first)

### 3. add-event-display
**Files to create/modify:**
- `src/tui/event_display.py` - EventDisplay class
- `src/tui/calendar.py` - CalendarView class (simple week view)

**Implementation:**
- Event panels grouped by date
- Time-sorted event list
- Simple week calendar view showing days with events
- Color-coded by category/priority
