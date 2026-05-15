import pytest
from src.services.engine import AnalyticsEngine
from src.models.schemas import WebEvent, ClientDevice
from datetime import datetime, timezone

@pytest.fixture
def test_engine():
    return AnalyticsEngine()

@pytest.fixture
def sample_event():
    device = ClientDevice(
        user_agent="Mozilla/5.0",
        screen_resolution="1920x1080",
        viewport="1920x900",
        language="en-US"
    )
    return WebEvent(
        event_id="evt_123",
        session_id="sess_abc",
        timestamp=datetime.now(timezone.utc).isoformat(),
        event_type="pageview",
        url="https://enterprise.com/home",
        device_metrics=device
    )

def test_ingestion(test_engine, sample_event):
    success = test_engine.ingest_event(sample_event)
    assert success is True
    assert len(test_engine.memory_buffer) == 1

def test_empty_metrics(test_engine):
    result = test_engine.calculate_metrics(5)
    assert result.total_pageviews == 0
    assert result.unique_visitors == 0
