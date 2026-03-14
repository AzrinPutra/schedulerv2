"""Notion API client."""

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import date, datetime


NOTION_API_URL = "https://api.notion.com/v1"


@dataclass
class NotionConfig:
    """Configuration for Notion integration."""
    api_key: str = ""
    database_id: str = ""
    
    @classmethod
    def from_env(cls) -> "NotionConfig":
        """Load config from environment variables."""
        return cls(
            api_key=os.getenv("NOTION_API_KEY", ""),
            database_id=os.getenv("NOTION_DATABASE_ID", ""),
        )
    
    def is_configured(self) -> bool:
        """Check if the config has required fields."""
        return bool(self.api_key and self.database_id)


class NotionClient:
    """Client for interacting with Notion API."""
    
    def __init__(self, config: NotionConfig):
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make an API request to Notion."""
        import urllib.request
        import json
        
        url = f"{NOTION_API_URL}{endpoint}"
        request_data = json.dumps(data).encode("utf-8") if data else None
        
        req = urllib.request.Request(
            url,
            data=request_data,
            headers=self.headers,
            method=method,
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            raise Exception(f"Notion API error: {e.code} - {error_body}")
    
    def query_database(
        self,
        database_id: str,
        filter: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
    ) -> List[Dict]:
        """Query a Notion database."""
        data = {}
        if filter:
            data["filter"] = filter
        if sorts:
            data["sorts"] = sorts
        
        result = self._make_request(
            "POST",
            f"/databases/{database_id}/query",
            data if data else None,
        )
        return result.get("results", [])
    
    def create_page(
        self,
        database_id: str,
        properties: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create a new page in a Notion database."""
        data = {
            "parent": {"database_id": database_id},
            "properties": properties,
        }
        return self._make_request("POST", "/pages", data)
    
    def update_page(
        self,
        page_id: str,
        properties: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Update a page's properties."""
        data = {"properties": properties}
        return self._make_request("PATCH", f"/pages/{page_id}", data)
    
    def delete_page(self, page_id: str) -> Dict[str, Any]:
        """Move a page to trash."""
        return self.update_page(page_id, {"archived": True})
    
    def get_page(self, page_id: str) -> Dict[str, Any]:
        """Get a page by ID."""
        return self._make_request("GET", f"/pages/{page_id}")
    
    def get_databases(self) -> List[Dict]:
        """List accessible databases."""
        result = self._make_request("GET", "/databases")
        return result.get("results", [])
