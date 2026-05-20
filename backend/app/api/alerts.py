from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import get_current_active_user, require_admin
from ..models import User, Alert
from ..schemas import AlertResponse

router = APIRouter()


@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    only_active: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Alert)
    if only_active:
        query = query.filter(Alert.is_resolved == False)
    alerts = query.order_by(Alert.created_at.desc()).all()
    return [AlertResponse.model_validate(a) for a in alerts]


@router.put("/alerts/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_resolved = True
    db.commit()
    db.refresh(alert)
    
    return AlertResponse.model_validate(alert)
