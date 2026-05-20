from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.models import User, Device, DevicePort, MonitorData, Alert
from app.core.security import get_password_hash
from app.api import api_router
import random
from datetime import datetime, timedelta

app = FastAPI(title="NetManager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if not db.query(User).first():
            admin_user = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                role="admin"
            )
            viewer_user = User(
                username="viewer",
                hashed_password=get_password_hash("viewer123"),
                role="viewer"
            )
            db.add(admin_user)
            db.add(viewer_user)
            db.commit()
        
        if not db.query(Device).first():
            vendors = ["Cisco", "Juniper", "Huawei", "Arista"]
            models = {
                "Cisco": ["Catalyst 9300", "ISR 4331", "ASR 9001"],
                "Juniper": ["EX4300", "MX204", "QFX5120"],
                "Huawei": ["S5735", "AR6509", "NE40E"],
                "Arista": ["7050X3", "7280R3", "7500R3"]
            }
            
            for i in range(1, 6):
                vendor = random.choice(vendors)
                model = random.choice(models[vendor])
                device = Device(
                    name=f"CoreSwitch-{i:02d}",
                    ip=f"192.168.1.{10 + i}",
                    model=model,
                    vendor=vendor,
                    snmp_version="v2c",
                    snmp_community="public",
                    ssh_user="admin",
                    ssh_password="secret",
                    status=random.choice(["online", "online", "offline"]),
                    location=f"Data Center Row {i}",
                    notes=f"Sample network device {i}"
                )
                db.add(device)
                db.commit()
                db.refresh(device)
                
                for j in range(1, 9):
                    port = DevicePort(
                        device_id=device.id,
                        port_name=f"Gi0/{j}",
                        description=f"Uplink Port {j}",
                        vlan=10 * j,
                        status="up" if j <= 4 else "down",
                        speed="1Gbps",
                        rx_bytes=random.randint(1000000, 1000000000),
                        tx_bytes=random.randint(1000000, 1000000000)
                    )
                    db.add(port)
                
                for h in range(24):
                    metric_time = datetime.utcnow() - timedelta(hours=h)
                    metric = MonitorData(
                        device_id=device.id,
                        cpu_usage=random.uniform(20, 80),
                        mem_usage=random.uniform(40, 90),
                        temperature=random.uniform(35, 55),
                        recorded_at=metric_time
                    )
                    db.add(metric)
                
                if random.random() > 0.5:
                    alert = Alert(
                        device_id=device.id,
                        alert_type="high_cpu",
                        message=f"High CPU usage detected on {device.name}",
                        severity="warning",
                        is_resolved=False
                    )
                    db.add(alert)
            
            db.commit()
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to NetManager API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
