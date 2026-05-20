from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_devices: int
    online_devices: int
    offline_devices: int
    active_alerts: int
