from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    ip = Column(String(45), nullable=False)
    model = Column(String(100))
    vendor = Column(String(50))
    snmp_version = Column(String(10))
    snmp_community = Column(String(100))
    ssh_user = Column(String(50))
    ssh_password = Column(String(255))
    status = Column(String(20), default="offline")
    location = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    configs = relationship("DeviceConfig", back_populates="device", cascade="all, delete-orphan")
    ports = relationship("DevicePort", back_populates="device", cascade="all, delete-orphan")
    monitor_data = relationship("MonitorData", back_populates="device", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="device", cascade="all, delete-orphan")


class DeviceConfig(Base):
    __tablename__ = "device_configs"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    config_text = Column(Text)
    version = Column(Integer, default=1)
    backup_time = Column(DateTime(timezone=True), server_default=func.now())

    device = relationship("Device", back_populates="configs")


class DevicePort(Base):
    __tablename__ = "device_ports"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    port_name = Column(String(50), nullable=False)
    description = Column(String(255))
    vlan = Column(Integer)
    status = Column(String(20))
    speed = Column(String(20))
    rx_bytes = Column(BigInteger, default=0)
    tx_bytes = Column(BigInteger, default=0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    device = relationship("Device", back_populates="ports")
