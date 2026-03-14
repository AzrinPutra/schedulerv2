# Plan: create-git-integration

## Intent Overview
Automate Git/GitHub backup for schedule data with scheduled exports.

## Goals
- Automatic git commits
- GitHub push support
- Backup script automation
- Schedule export to markdown

## Work Items

### 1. create-git-automation
**Files to create:**
- `src/git/__init__.py` - Package exports
- `src/git/automation.py` - Git automation class

**Implementation:**
- GitAutomation class for auto-commits
- Track changes, add, commit, push methods
- Configurable commit messages

### 2. create-github-integration  
**Files to create:**
- `src/git/github.py` - GitHub integration

**Implementation:**
- GitHub integration using gh CLI
- Create/manage repository
- Push commits to remote

### 3. create-markdown-export
**Files to create:**
- `src/git/export.py` - Schedule export to markdown

**Implementation:**
- Export tasks/events to formatted markdown
- Daily/weekly schedule summaries
- Grouped by date/category
