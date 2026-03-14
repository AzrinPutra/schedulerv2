# Work Item: Add serialization

**ID**: add-serialization  
**Intent**: create-schedule-data-models  
**Status**: pending  
**Complexity**: medium  
**Mode**: confirm

## Description

Add methods to serialize models to and from dictionaries for storage.

## Files to Modify

- `src/models/schedule.py` - Add to_dict/from_dict methods
- `src/models/types.py` - Add serialization helpers

## Requirements

- Dictionary representation for each model
- Ability to recreate objects from dictionaries
- Handle datetime objects properly
- Support JSON serialization

## Acceptance Criteria

- Each model has to_dict() method
- Each model has from_dict() class method
- Object recreation works correctly
- Datetime objects serialize/deserialize properly
