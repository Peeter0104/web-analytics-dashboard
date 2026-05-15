from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any

class ClientDevice(BaseModel):
    user_agent: str
    screen_resolution: str
    viewport: str
    language: str

class WebEvent(BaseModel):
    event_id: str
    session_id: str
    timestamp: str
    event_type: str
    url: HttpUrl
    referrer: Optional[HttpUrl] = None
    device_metrics: ClientDevice
    custom_properties: Optional[Dict[str, Any]] = None

class AggregationResult(BaseModel):
    time_window: str
    total_pageviews: int
    unique_visitors: int
    bounce_rate: float
    avg_session_duration: float
