from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    alert_type = Column(String(50))
    message = Column(Text)
    severity = Column(String(20))
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    device = relationship("Device", back_populates="alerts")
