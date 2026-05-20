from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MonitorDataResponse(BaseModel):
    id: int
    device_id: int
    cpu_usage: Optional[float] = None
    mem_usage: Optional[float] = None
    temperature: Optional[float] = None
    recorded_at: datetime

    model_config = {
        "from_attributes": True
    }
