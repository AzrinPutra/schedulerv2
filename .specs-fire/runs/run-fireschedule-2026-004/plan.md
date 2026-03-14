# Plan: Run for add-serialization work item

**Work Item ID**: add-serialization  
**Intent**: create-schedule-data-models  
**Mode**: confirm  
**Date**: 2026-03-14T13:00:00Z

## Objective

Add serialization methods to enable models to be converted to/from dictionaries for storage.

## Proposed Implementation

### Files to Create/Modify

1. `src/models/serialization.py` - New file for serialization utilities
2. `src/models/schedule.py` - Add to_dict/from_dict methods to all models
3. `src/models/__init__.py` - Export serialization utilities

### Serialization Requirements

1. **to_dict()** - Convert model instance to dictionary
   - Handle datetime objects (ISO format strings)
   - Handle date objects (ISO format strings)
   - Handle time objects (ISO format strings)
   - Handle enum objects (value strings)
   - Handle None values

2. **from_dict()** - Create model instance from dictionary
   - Parse ISO format strings back to datetime/date/time
   - Convert enum value strings back to enum members
   - Handle missing optional fields

3. **Utility Functions**
   - `datetime_to_iso()` / `datetime_from_iso()`
   - `date_to_iso()` / `date_from_iso()`
   - `time_to_iso()` / `time_from_iso()`
   - `enum_to_value()` / `enum_from_value()`

### Implementation Approach

```python
# Example pattern for models
@dataclass
class Task(BaseModel):
    ...
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "due_date": date_to_iso(self.due_date) if self.due_date else None,
            "category": self.category.value,
            ...
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Task:
        """Create model from dictionary."""
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            due_date=date_from_iso(data.get("due_date")) if data.get("due_date") else None,
            category=Category(data.get("category", "personal")),
            ...
        )
```

## Dependencies

- datetime (for ISO format conversion)
- typing (for type hints)
- Existing enums (Category, Priority, Status)

## Expected Outcome

- All models can serialize to dictionaries
- All models can be recreated from dictionaries
- Round-trip serialization preserves all data
- Ready for JSON/markdown storage integration

## Test Plan

1. Test to_dict() produces correct dictionary
2. Test from_dict() recreates object correctly
3. Test round-trip (to_dict -> from_dict -> to_dict)
4. Test with None values
5. Test with all enum values

Please confirm this plan to proceed with implementation.
