from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from ..core.database import get_db
from ..core.security import get_current_active_user, require_admin
from ..models import User, Device, DeviceConfig, DevicePort, MonitorData, Alert, OperationLog
from ..schemas import (
    DeviceCreate, DeviceUpdate, DeviceResponse,
    DeviceConfigResponse, DevicePortResponse, MonitorDataResponse
)
import random
from datetime import datetime, timedelta

router = APIRouter()


def create_operation_log(db: Session, user_id: int, action: str, target_type: str, target_id: int, details: str):
    log = OperationLog(
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        details=details
    )
    db.add(log)
    db.commit()


@router.get("/devices", response_model=List[DeviceResponse])
async def get_devices(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    vendor: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Device)
    
    if search:
        query = query.filter(
            or_(
                Device.name.contains(search),
                Device.ip.contains(search),
                Device.model.contains(search)
            )
        )
    
    if vendor:
        query = query.filter(Device.vendor == vendor)
    
    if status:
        query = query.filter(Device.status == status)
    
    devices = query.offset(skip).limit(limit).all()
    return [DeviceResponse.model_validate(d) for d in devices]


@router.get("/devices/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return DeviceResponse.model_validate(device)


@router.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_device = Device(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    
    create_operation_log(db, current_user.id, "CREATE", "device", db_device.id, f"Created device {db_device.name}")
    
    for i in range(1, 5):
        port = DevicePort(
            device_id=db_device.id,
            port_name=f"Gi0/{i}",
            description=f"Port {i}",
            vlan=10 * i,
            status="up" if i % 2 == 0 else "down",
            speed="1Gbps",
            rx_bytes=random.randint(1000000, 100000000),
            tx_bytes=random.randint(1000000, 100000000)
        )
        db.add(port)
    db.commit()
    
    return DeviceResponse.model_validate(db_device)


@router.put("/devices/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: int,
    device_update: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    update_data = device_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_device, field, value)
    
    db.commit()
    db.refresh(db_device)
    
    create_operation_log(db, current_user.id, "UPDATE", "device", device_id, f"Updated device {db_device.name}")
    
    return DeviceResponse.model_validate(db_device)


@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(db_device)
    db.commit()
    
    create_operation_log(db, current_user.id, "DELETE", "device", device_id, f"Deleted device {db_device.name}")
    
    return None


@router.get("/devices/{device_id}/configs", response_model=List[DeviceConfigResponse])
async def get_device_configs(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    configs = db.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).order_by(DeviceConfig.backup_time.desc()).all()
    return [DeviceConfigResponse.model_validate(c) for c in configs]


@router.post("/devices/{device_id}/backup_config", response_model=DeviceConfigResponse)
async def backup_device_config(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    last_config = db.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).order_by(DeviceConfig.version.desc()).first()
    new_version = last_config.version + 1 if last_config else 1
    
    config_text = f"""! Configuration for {device.name}
! Version {new_version}
! Generated at {datetime.now()}
hostname {device.name}
interface Loopback0
 ip address 10.0.{device_id}.1 255.255.255.255
"""
    
    new_config = DeviceConfig(
        device_id=device_id,
        config_text=config_text,
        version=new_version
    )
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    
    create_operation_log(db, current_user.id, "BACKUP", "config", device_id, f"Backed up config for {device.name}")
    
    return DeviceConfigResponse.model_validate(new_config)


@router.get("/devices/{device_id}/ports", response_model=List[DevicePortResponse])
async def get_device_ports(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    ports = db.query(DevicePort).filter(DevicePort.device_id == device_id).all()
    return [DevicePortResponse.model_validate(p) for p in ports]


@router.get("/devices/{device_id}/metrics", response_model=List[MonitorDataResponse])
async def get_device_metrics(
    device_id: int,
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    since = datetime.utcnow() - timedelta(hours=hours)
    metrics = db.query(MonitorData).filter(
        and_(MonitorData.device_id == device_id, MonitorData.recorded_at >= since)
    ).order_by(MonitorData.recorded_at.asc()).all()
    
    return [MonitorDataResponse.model_validate(m) for m in metrics]
