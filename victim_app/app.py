import threading
import time
from typing import Any

import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import SOC_API_KEY, SOC_API_URL, SOURCE_NAME

app = FastAPI(title="Victim demo app", description="Login portal and traffic simulator → SOC log processor")

SOC_BACKEND_LOG = SOC_API_URL
SOC_BACKEND_HONEY = "http://127.0.0.1:8000/honeytokens/endpoints"

honey_endpoints: list[str] = []


def _client_ip(request: Request) -> str:
    client = request.client
    return client.host if client else "127.0.0.1"


def send_ingest_log(
    *,
    ip: str,
    endpoint: str,
    method: str,
    status: int,
    username: str | None = None,
    user_agent: str | None = None,
) -> bool:
    """Forward one log line to the main SOC /ingest-log (LogProcessor pipeline)."""
    log: dict[str, Any] = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source": SOURCE_NAME,
        "ip": ip,
        "endpoint": endpoint,
        "method": method,
        "status": status,
        "user_agent": user_agent or "",
        "username": username,
    }
    try:
        r = requests.post(
            SOC_BACKEND_LOG,
            json=log,
            headers={"Authorization": f"Bearer {SOC_API_KEY}"},
            timeout=3,
        )
        return r.ok
    except Exception:
        return False


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5174",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    path = request.url.path
    # /login sends a richer log (with username) from the handler — avoid duplicate.
    if path not in ("/login", "/health"):
        client = request.client
        log = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "source": SOURCE_NAME,
            "ip": client.host if client else "unknown",
            "endpoint": path,
            "method": request.method,
            "status": response.status_code,
            "user_agent": request.headers.get("user-agent"),
        }
        try:
            requests.post(
                SOC_BACKEND_LOG,
                json=log,
                headers={"Authorization": f"Bearer {SOC_API_KEY}"},
                timeout=2,
            )
        except Exception:
            pass
    return response


def fetch_honeytokens() -> None:
    global honey_endpoints
    while True:
        try:
            res = requests.get(SOC_BACKEND_HONEY, timeout=2)
            data = res.json()
            honey_endpoints = data.get("endpoint_traps", []) or data.get("active_honeytokens", []) or []
            if isinstance(honey_endpoints, list) and honey_endpoints and isinstance(honey_endpoints[0], dict):
                honey_endpoints = [t.get("endpoint", t.get("path", "")) for t in honey_endpoints if t]
            honey_endpoints = [str(e) for e in honey_endpoints if e]
        except Exception:
            pass
        time.sleep(30)


threading.Thread(target=fetch_honeytokens, daemon=True).start()


class LoginRequest(BaseModel):
    username: str = Field(default="", max_length=128)
    password: str = Field(default="", max_length=256)


@app.get("/health")
async def health():
    soc_ok = False
    try:
        r = requests.get("http://127.0.0.1:8000/system-status", timeout=1.5)
        soc_ok = r.ok
    except Exception:
        soc_ok = False
    return {"victim_api": "ok", "soc_reachable": soc_ok}


@app.get("/")
async def home():
    return {"message": "Victim demo API — use POST /login or the Vite UI on port 5174"}


@app.post("/login")
async def login(body: LoginRequest, request: Request):
    """
    Demo credentials (any other combo is treated as failed login → higher-risk telemetry):
    - demo / demo  → success
    - admin / password123 → success
    """
    ip = _client_ip(request)
    ua = request.headers.get("user-agent")
    u = (body.username or "").strip()
    p = body.password or ""
    ok = (u == "demo" and p == "demo") or (u == "admin" and p == "password123")
    status_code = 200 if ok else 401
    soc_logged = send_ingest_log(
        ip=ip,
        endpoint="/login",
        method="POST",
        status=status_code,
        username=u or None,
        user_agent=ua,
    )
    if ok:
        return {
            "status": "Signed in (demo user)",
            "soc_logged": soc_logged,
        }
    return {
        "status": "Invalid credentials",
        "soc_logged": soc_logged,
    }


@app.get("/admin")
async def admin():
    return {"status": "admin portal"}


@app.get("/config")
async def config_page():
    return {"status": "configuration page"}


@app.get("/debug-console")
async def debug():
    return {"status": "debug console"}


@app.get("/{path:path}")
async def honeytoken_route(path: str, request: Request):
    endpoint = "/" + path
    if endpoint in honey_endpoints:
        return {"error": "unauthorized access"}
    return {"message": "resource not found"}
