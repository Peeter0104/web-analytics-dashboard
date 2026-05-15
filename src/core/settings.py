import os
from pydantic import BaseModel

class DashboardSettings(BaseModel):
    application_name: str = "EnterpriseWebAnalytics"
    environment: str = os.getenv("ENV", "production")
    flush_interval_seconds: int = 60
    max_batch_size: int = 5000
    cors_origins: list[str] = ["*"]

config = DashboardSettings()
