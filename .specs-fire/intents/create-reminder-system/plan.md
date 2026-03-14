# Plan: create-reminder-system

## Intent Overview
Create a reminder system for tasks and events with configurable notifications.

## Goals
- Due date reminders for tasks
- Event notifications
- Daily schedule summary
- Configurable reminder times

## Work Items

### 1. create-reminder-model
**Files to create:**
- `src/reminder/__init__.py` - Package exports
- `src/reminder/models.py` - Reminder model
- `src/reminder/config.py` - ReminderConfig

**Implementation:**
- Reminder model: id, task_id/event_id, reminder_type, minutes_before, enabled
- ReminderConfig: default_minutes_before, notification_enabled, quiet_hours

### 2. create-reminder-service  
**Files to create:**
- `src/reminder/service.py` - ReminderService class

**Implementation:**
- Check due dates and send notifications
- Event start reminders
- Daily schedule summary
- CLI notifications using Rich
