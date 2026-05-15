from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.models.schemas import WebEvent, AggregationResult
from src.services.engine import AnalyticsEngine

router = APIRouter()
engine = AnalyticsEngine()

@router.post("/collect", status_code=202)
def track_event(event: WebEvent, background_tasks: BackgroundTasks):
    if not event.event_id:
        raise HTTPException(status_code=400, detail="Missing event identifier")
    
    background_tasks.add_task(engine.ingest_event, event)
    return {"status": "accepted", "event_id": event.event_id}

@router.get("/metrics/realtime", response_model=AggregationResult)
def get_realtime_dashboard():
    metrics = engine.calculate_metrics(window_minutes=5)
    return metrics
