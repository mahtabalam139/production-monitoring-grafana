from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from prometheus_client import make_asgi_app

from backend.api.home import router as home_router
from backend.api.system import router as system_router
from backend.api.resources import router as resources_router
from backend.api.dashboard import router as dashboard_router
from backend.api.system_page import router as system_page_router
from backend.api.process import router as process_router
from backend.api.docker import router as docker_router
from backend.api.database import router as database_router
from backend.api.logs import router as logs_router
from backend.api.alerts import router as alerts_router
from backend.api.servers import router as servers_router

app = FastAPI(
    title="Production Monitoring Dashboard",
    description="Enterprise Monitoring System",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(home_router)
app.include_router(system_router)
app.include_router(resources_router)
app.include_router(dashboard_router)
app.include_router(system_page_router)
app.include_router(process_router)
app.include_router(docker_router)
app.include_router(database_router)
app.include_router(logs_router)
app.include_router(alerts_router)
app.include_router(servers_router)