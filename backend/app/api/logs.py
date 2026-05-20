from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import get_current_active_user
from ..models import User, OperationLog
from ..schemas import OperationLogResponse

router = APIRouter()


@router.get("/logs", response_model=List[OperationLogResponse])
async def get_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    logs = db.query(OperationLog).order_by(OperationLog.created_at.desc()).offset(skip).limit(limit).all()
    return [OperationLogResponse.model_validate(l) for l in logs]
