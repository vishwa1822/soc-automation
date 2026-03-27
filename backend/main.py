from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from api.log_api import router as log_router
from api.dashboard_honeytokens_api import router as honey_router
from api.system_api import router as system_router
from api.dashboard_api import router as dashboard_router
from api.soc_ai_api import router as soc_ai_router


app = FastAPI(title="AI SOC Automation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(log_router)
app.include_router(honey_router)
app.include_router(system_router)
app.include_router(dashboard_router)
app.include_router(soc_ai_router)

# Serve built frontend (Vite) from / (Option A)
frontend_dist = Path(__file__).resolve().parents[1] / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")