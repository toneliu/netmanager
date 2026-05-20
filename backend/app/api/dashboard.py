from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..core.database import get_db
from ..core.security import get_current_active_user
from ..models import User, Device, Alert
from ..schemas import DashboardStats

router = APIRouter()


@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    total_devices = db.query(func.count(Device.id)).scalar() or 0
    online_devices = db.query(func.count(Device.id)).filter(Device.status == "online").scalar() or 0
    offline_devices = db.query(func.count(Device.id)).filter(Device.status == "offline").scalar() or 0
    active_alerts = db.query(func.count(Alert.id)).filter(Alert.is_resolved == False).scalar() or 0
    
    return DashboardStats(
        total_devices=total_devices,
        online_devices=online_devices,
        offline_devices=offline_devices,
        active_alerts=active_alerts
    )
