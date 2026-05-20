from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OperationLogResponse(BaseModel):
    id: int
    user_id: int
    action: Optional[str] = None
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    details: Optional[str] = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
