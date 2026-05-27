import os
import warnings

# FAISS (SWIG) emits harmless DeprecationWarnings on Python 3.12+ — not an app bug.
for _prefix in (
    "builtin type SwigPyPacked",
    "builtin type SwigPyObject",
    "builtin type swigvarlink",
):
    warnings.filterwarnings("ignore", message=_prefix, category=DeprecationWarning)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from api.log_api import router as log_router
from api.dashboard_honeytokens_api import router as honey_router
from api.system_api import router as system_router
from api.dashboard_api import router as dashboard_router
from api.soc_ai_api import router as soc_ai_router
from api.soar_api import router as soar_router


app = FastAPI(title="AI SOC Automation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:5174",
        "http://localhost:5174",
        "http://127.0.0.1:4173",
        "http://localhost:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(log_router)
app.include_router(soar_router)
app.include_router(honey_router)
app.include_router(system_router)
app.include_router(dashboard_router)
app.include_router(soc_ai_router)

# Serve built SPA from the API only when explicitly enabled (avoids a second dashboard on :8000
# during dev while Vite runs on :5173 / victim UI on :5174).
# Production / single-port: build frontend then run with SOC_SERVE_FRONTEND=1
frontend_dist = Path(__file__).resolve().parents[1] / "frontend" / "dist"
if os.environ.get("SOC_SERVE_FRONTEND", "").strip().lower() in ("1", "true", "yes") and frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")