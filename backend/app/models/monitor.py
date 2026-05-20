from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class MonitorData(Base):
    __tablename__ = "monitor_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    cpu_usage = Column(Float)
    mem_usage = Column(Float)
    temperature = Column(Float)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    device = relationship("Device", back_populates="monitor_data")
