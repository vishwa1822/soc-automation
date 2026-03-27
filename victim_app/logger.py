import requests
import datetime

SOC_LOG_API = "http://localhost:8000/api/logs"


def send_log(event_type, resource, ip):

    log = {
        "timestamp": str(datetime.datetime.utcnow()),
        "event_type": event_type,
        "resource": resource,
        "ip": ip
    }

    try:
        requests.post(SOC_LOG_API, json=log)
    except Exception:
        pass