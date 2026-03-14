"""Google Calendar sync service for bi-directional sync with scheduler."""

from typing import Optional, Dict, Any, List
from datetime import datetime, date, time, timedelta

from .client import GoogleCalendarClient, GoogleCalendarConfig
from ...models import Task, Event, Category, Priority, Status
from ...storage import MarkdownStorage


class GoogleCalendarSync:
    """Sync service between scheduler and Google Calendar."""
    
    def __init__(
        self,
        storage: MarkdownStorage,
        config: Optional[GoogleCalendarConfig] = None,
    ):
        self.storage = storage
        self.config = config or GoogleCalendarConfig.from_env()
        self.client = GoogleCalendarClient(self.config)
    
    def is_configured(self) -> bool:
        """Check if Google Calendar integration is configured."""
        return self.client.is_configured()
    
    def event_to_google_format(self, event: Event) -> Dict[str, Any]:
        """Convert an Event to Google Calendar format."""
        google_event = {
            "summary": event.title,
            "description": event.description or "",
        }
        
        if event.date_field and event.time:
            start_datetime = datetime.combine(event.date_field, event.time)
            end_datetime = start_datetime + timedelta(
                minutes=event.duration_minutes or 60
            )
            
            google_event["start"] = {
                "dateTime": start_datetime.isoformat(),
                "timeZone": "UTC",
            }
            google_event["end"] = {
                "dateTime": end_datetime.isoformat(),
                "timeZone": "UTC",
            }
        elif event.date_field:
            google_event["start"] = {
                "date": event.date_field.isoformat(),
            }
            google_event["end"] = {
                "date": event.date_field.isoformat(),
            }
        
        return google_event
    
    def google_format_to_event(self, google_event: Dict) -> Optional[Event]:
        """Convert Google Calendar event to scheduler Event."""
        summary = google_event.get("summary", "")
        if not summary:
            return None
        
        start = google_event.get("start", {})
        end = google_event.get("end", {})
        
        event_date = date.today()
        event_time = None
        duration = 60
        
        if "dateTime" in start:
            try:
                start_dt = datetime.fromisoformat(start["dateTime"].replace("Z", "+00:00"))
                event_date = start_dt.date()
                event_time = start_dt.time()
                
                if "dateTime" in end:
                    end_dt = datetime.fromisoformat(end["dateTime"].replace("Z", "+00:00"))
                    duration = int((end_dt - start_dt).total_seconds() / 60)
            except (ValueError, TypeError):
                pass
        elif "date" in start:
            try:
                event_date = datetime.strptime(start["date"], "%Y-%m-%d").date()
            except ValueError:
                pass
        
        google_id = google_event.get("id", "")
        
        return Event(
            id=f"gcal_{google_id}",
            title=summary,
            description=google_event.get("description"),
            date_field=event_date,
            time=event_time,
            duration_minutes=duration if duration > 0 else 60,
            category=Category.PERSONAL,
            priority=Priority.MEDIUM,
            status=Status.PENDING,
        )
    
    def push_event(self, event: Event) -> str:
        """Push an event to Google Calendar. Returns Google event ID."""
        if not self.client.is_configured():
            raise RuntimeError("Google Calendar is not configured")
        
        google_event = self.event_to_google_format(event)
        result = self.client.create_event(google_event)
        return result.get("id", "")
    
    def pull_events(
        self,
        days_ahead: int = 7,
    ) -> List[Event]:
        """Pull events from Google Calendar."""
        if not self.client.is_configured():
            raise RuntimeError("Google Calendar is not configured")
        
        now = datetime.now()
        time_max = now + timedelta(days=days_ahead)
        
        google_events = self.client.list_events(now, time_max)
        
        events = []
        for gcal_event in google_events:
            event = self.google_format_to_event(gcal_event)
            if event:
                events.append(event)
        
        return events
    
    def sync_to_google(self) -> Dict[str, int]:
        """Sync all local events to Google Calendar. Returns stats."""
        if not self.client.is_configured():
            raise RuntimeError("Google Calendar is not configured")
        
        local_events = self.storage.list_all_events()
        pushed = 0
        
        for event in local_events:
            try:
                self.push_event(event)
                pushed += 1
            except Exception:
                pass
        
        return {"pushed": pushed}
    
    def sync_from_google(self, days_ahead: int = 7) -> Dict[str, int]:
        """Sync events from Google Calendar to local storage. Returns stats."""
        if not self.client.is_configured():
            raise RuntimeError("Google Calendar is not configured")
        
        google_events = self.pull_events(days_ahead)
        imported = 0
        
        for event in google_events:
            event.id = event.id.replace("gcal_", "")
            self.storage.save(event)
            imported += 1
        
        return {"imported": imported}
    
    def full_sync(self, days_ahead: int = 7) -> Dict[str, int]:
        """Perform full bi-directional sync."""
        from_google = self.sync_from_google(days_ahead)
        to_google = self.sync_to_google()
        
        return {
            "imported": from_google.get("imported", 0),
            "pushed": to_google.get("pushed", 0),
        }
