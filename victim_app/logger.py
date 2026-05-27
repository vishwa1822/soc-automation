import requests
import datetime

from config import SOC_API_KEY, SOC_API_URL, SOURCE_NAME


def send_log(event_type, resource, ip):

    log = {
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
        "source": SOURCE_NAME,
        "ip": ip,
        "endpoint": resource,
        "method": "GET",
        "status": 200,
        "user_agent": f"victim-background ({event_type})",
    }

    try:
        requests.post(
            SOC_API_URL,
            json=log,
            headers={"Authorization": f"Bearer {SOC_API_KEY}"},
            timeout=2,
        )
    except Exception:
        pass