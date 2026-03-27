import requests
import time

from config import SOC_API_URL, SOC_API_KEY, SOURCE_NAME


class LoggingMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):

        if scope["type"] == "http":

            endpoint = scope["path"]
            method = scope["method"]

            client = scope.get("client")
            ip = client[0] if client else "unknown"

            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")

            log_data = {
                "timestamp": timestamp,
                "source": SOURCE_NAME,
                "ip": ip,
                "endpoint": endpoint,
                "method": method
            }

            try:

                requests.post(
                    SOC_API_URL,
                    json=log_data,
                    headers={
                        "Authorization": f"Bearer {SOC_API_KEY}"
                    },
                    timeout=1
                )

            except Exception:
                pass

        await self.app(scope, receive, send)