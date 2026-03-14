"""Type definitions for the scheduler."""

from typing import Dict, List, Optional, Union, Any
from datetime import datetime, date, time

# Type aliases for clarity
TaskId = str
EventId = str
ScheduleItemId = str
UserId = str

# Common data structures
ScheduleData = Dict[str, Any]
SerializedModel = Dict[str, Any]

# Date/time types
DateStr = str  # Format: YYYY-MM-DD
TimeStr = str  # Format: HH:MM
