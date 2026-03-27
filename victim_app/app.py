from fastapi import FastAPI, Request
import requests
import time
import threading

app = FastAPI()

SOC_BACKEND_LOG = "http://127.0.0.1:8000/api/logs"
SOC_BACKEND_HONEY = "http://127.0.0.1:8000/honeytokens/endpoints"

# store active honey endpoints
honey_endpoints = []


# ---------------------------------
# Send log to SOC backend
# ---------------------------------
async def send_log(request: Request):

    log = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "demo-webapp",
        "ip": request.client.host,
        "endpoint": request.url.path,
        "method": request.method,
        "user_agent": request.headers.get("user-agent")
    }

    try:
        requests.post(SOC_BACKEND_LOG, json=log, timeout=1)
    except:
        pass


# ---------------------------------
# Logging middleware
# ---------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):

    await send_log(request)

    response = await call_next(request)

    return response


# ---------------------------------
# Fetch honeytokens from SOC
# ---------------------------------
def fetch_honeytokens():

    global honey_endpoints

    while True:

        try:

            res = requests.get(SOC_BACKEND_HONEY, timeout=2)

            data = res.json()

            honey_endpoints = data.get("endpoint_traps", [])

            print("[Victim App] Updated honey endpoints:", honey_endpoints)

        except:
            pass

        time.sleep(30)


# start background fetch thread
threading.Thread(target=fetch_honeytokens, daemon=True).start()


# ---------------------------------
# Normal endpoints
# ---------------------------------
@app.get("/")
async def home():
    return {"message": "welcome to demo web application"}


@app.post("/login")
async def login():
    return {"status": "invalid credentials"}


@app.get("/admin")
async def admin():
    return {"status": "admin portal"}


@app.get("/config")
async def config():
    return {"status": "configuration page"}


@app.get("/debug-console")
async def debug():
    return {"status": "debug console"}


# ---------------------------------
# Honeytoken catch-all
# ---------------------------------
@app.get("/{path:path}")
async def honeytoken_route(path: str, request: Request):

    endpoint = "/" + path

    if endpoint in honey_endpoints:

        print("[Victim App] Honeytoken accessed:", endpoint)

        return {"error": "unauthorized access"}

    return {"message": "resource not found"}