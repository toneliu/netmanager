from fastapi import APIRouter
from .auth import router as auth_router
from .devices import router as devices_router
from .dashboard import router as dashboard_router
from .alerts import router as alerts_router
from .logs import router as logs_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(devices_router, tags=["devices"])
api_router.include_router(dashboard_router, tags=["dashboard"])
api_router.include_router(alerts_router, tags=["alerts"])
api_router.include_router(logs_router, tags=["logs"])
