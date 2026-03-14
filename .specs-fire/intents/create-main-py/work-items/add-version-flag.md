# Work Item: Add version flag

**ID**: add-version-flag  
**Intent**: create-main-py  
**Status**: pending  
**Complexity**: low  
**Mode**: autopilot

## Description

Add `--version` flag to CLI that displays version from `src/__init__.py`.

## Files to Create/Modify

- `src/cli.py` - Add version command/flag

## Acceptance Criteria

- `scheduler --version` displays version
- Version comes from `src/__init__.py`
