from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DeviceBase(BaseModel):
    name: str
    ip: str
    model: Optional[str] = None
    vendor: Optional[str] = None
    snmp_version: Optional[str] = None
    snmp_community: Optional[str] = None
    ssh_user: Optional[str] = None
    ssh_password: Optional[str] = None
    status: Optional[str] = "offline"
    location: Optional[str] = None
    notes: Optional[str] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    name: Optional[str] = None
    ip: Optional[str] = None


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class DeviceConfigResponse(BaseModel):
    id: int
    device_id: int
    config_text: Optional[str] = None
    version: int
    backup_time: datetime

    model_config = {
        "from_attributes": True
    }


class DevicePortResponse(BaseModel):
    id: int
    device_id: int
    port_name: str
    description: Optional[str] = None
    vlan: Optional[int] = None
    status: Optional[str] = None
    speed: Optional[str] = None
    rx_bytes: Optional[int] = None
    tx_bytes: Optional[int] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
