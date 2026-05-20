from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlertResponse(BaseModel):
    id: int
    device_id: int
    alert_type: Optional[str] = None
    message: Optional[str] = None
    severity: Optional[str] = None
    is_resolved: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
