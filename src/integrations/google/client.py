"""Google Calendar API client."""

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, date, time


CALENDAR_API_URL = "https://www.googleapis.com/calendar/v3"


@dataclass
class GoogleCalendarConfig:
    """Configuration for Google Calendar integration."""
    credentials_path: str = ""
    token_path: str = ""
    calendar_id: str = "primary"
    
    @classmethod
    def from_env(cls) -> "GoogleCalendarConfig":
        """Load config from environment variables."""
        return cls(
            credentials_path=os.getenv("GOOGLE_CREDENTIALS_PATH", ""),
            token_path=os.getenv("GOOGLE_TOKEN_PATH", ""),
            calendar_id=os.getenv("GOOGLE_CALENDAR_ID", "primary"),
        )
    
    def is_configured(self) -> bool:
        """Check if the config has required fields."""
        return bool(self.credentials_path and os.path.exists(self.credentials_path))


class GoogleCalendarClient:
    """Client for interacting with Google Calendar API."""
    
    def __init__(self, config: GoogleCalendarConfig):
        self.config = config
        self.service = None
        self._init_service()
    
    def _init_service(self) -> None:
        """Initialize the Google Calendar service."""
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            creds = None
            
            if self.config.token_path and os.path.exists(self.config.token_path):
                creds = Credentials.from_authorized_user_file(
                    self.config.token_path,
                    ["https://www.googleapis.com/auth/calendar"]
                )
            
            if not creds and self.config.credentials_path:
                from google.auth.transport.requests import Request
                from google.oauth2 import ServiceAccountCredentials
                import json
                
                with open(self.config.credentials_path) as f:
                    creds_dict = json.load(f)
                
                creds = ServiceAccountCredentials.from_service_account_info(
                    creds_dict,
                    scopes=["https://www.googleapis.com/auth/calendar"]
                )
            
            if creds:
                self.service = build("calendar", "v3", credentials=creds)
        except ImportError:
            self.service = None
        except Exception:
            self.service = None
    
    def is_configured(self) -> bool:
        """Check if Google Calendar is configured."""
        return self.service is not None
    
    def list_events(
        self,
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 100,
    ) -> List[Dict]:
        """List events from the calendar."""
        if not self.service:
            return []
        
        if time_min is None:
            time_min = datetime.now()
        if time_max is None:
            time_max = datetime.now().replace(hour=23, minute=59, second=59)
        
        try:
            events_result = self.service.events().list(
                calendarId=self.config.calendar_id,
                timeMin=time_min.isoformat() + "Z",
                timeMax=time_max.isoformat() + "Z",
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            
            return events_result.get("items", [])
        except Exception:
            return []
    
    def create_event(self, event: Dict) -> Dict:
        """Create a new calendar event."""
        if not self.service:
            raise RuntimeError("Google Calendar is not configured")
        
        return self.service.events().insert(
            calendarId=self.config.calendar_id,
            body=event,
        ).execute()
    
    def update_event(self, event_id: str, event: Dict) -> Dict:
        """Update an existing event."""
        if not self.service:
            raise RuntimeError("Google Calendar is not configured")
        
        return self.service.events().update(
            calendarId=self.config.calendar_id,
            eventId=event_id,
            body=event,
        ).execute()
    
    def delete_event(self, event_id: str) -> bool:
        """Delete an event."""
        if not self.service:
            return False
        
        try:
            self.service.events().delete(
                calendarId=self.config.calendar_id,
                eventId=event_id,
            ).execute()
            return True
        except Exception:
            return False
    
    def get_event(self, event_id: str) -> Optional[Dict]:
        """Get a specific event."""
        if not self.service:
            return None
        
        try:
            return self.service.events().get(
                calendarId=self.config.calendar_id,
                eventId=event_id,
            ).execute()
        except Exception:
            return None
