# Work Item: Add validation

**ID**: add-validation  
**Intent**: create-schedule-data-models  
**Status**: pending  
**Complexity**: medium  
**Mode**: confirm

## Description

Add validation methods to ensure data integrity for all models.

## Files to Modify

- `src/models/schedule.py` - Add validation methods
- `src/models/types.py` - Add validation helpers

## Requirements

- Validation using Pydantic or custom methods
- Ensure required fields are present
- Validate date/time formats
- Validate enum values

## Acceptance Criteria

- All models have validation methods
- Invalid data raises appropriate exceptions
- Validation occurs during model creation
