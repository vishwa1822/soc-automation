from collections import defaultdict
import time


class EnumerationDetector:

    def __init__(self):

        self.requests = defaultdict(list)

    def detect(self, log):

        ip = log.get("ip")
        endpoint = log.get("endpoint")

        now = time.time()

        self.requests[ip].append((endpoint, now))

        recent = [
            r for r in self.requests[ip]
            if now - r[1] < 30
        ]

        self.requests[ip] = recent

        if len(recent) > 10:

            return {
                "enumeration": True,
                "count": len(recent)
            }

        return {
            "enumeration": False
        }