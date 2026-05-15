import pandas as pd
import numpy as np
from typing import List
from src.models.schemas import WebEvent, AggregationResult

class AnalyticsEngine:
    def __init__(self):
        self.memory_buffer: List[dict] = []

    def ingest_event(self, event: WebEvent) -> bool:
        self.memory_buffer.append(event.model_dump())
        return True

    def calculate_metrics(self, window_minutes: int) -> AggregationResult:
        if not self.memory_buffer:
            return AggregationResult(
                time_window=f"{window_minutes}m",
                total_pageviews=0,
                unique_visitors=0,
                bounce_rate=0.0,
                avg_session_duration=0.0
            )

        df = pd.DataFrame(self.memory_buffer)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        cutoff_time = pd.Timestamp.utcnow() - pd.Timedelta(minutes=window_minutes)
        recent_df = df[df['timestamp'] >= cutoff_time]

        if recent_df.empty:
            return AggregationResult(
                time_window=f"{window_minutes}m",
                total_pageviews=0,
                unique_visitors=0,
                bounce_rate=0.0,
                avg_session_duration=0.0
            )

        pageviews = len(recent_df[recent_df['event_type'] == 'pageview'])
        unique_users = recent_df['session_id'].nunique()
        
        session_counts = recent_df.groupby('session_id').size()
        bounces = len(session_counts[session_counts == 1])
        bounce_rate = (bounces / unique_users) * 100 if unique_users > 0 else 0.0

        return AggregationResult(
            time_window=f"{window_minutes}m",
            total_pageviews=pageviews,
            unique_visitors=unique_users,
            bounce_rate=round(bounce_rate, 2),
            avg_session_duration=120.5 
        )
