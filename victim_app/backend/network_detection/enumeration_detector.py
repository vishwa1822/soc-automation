import time


class EnumerationDetector:

    def __init__(self):

        self.request_log = {}

        self.threshold = 10
        self.window = 30  # seconds

    def detect(self, log):

        ip = log.get("ip")
        endpoint = log.get("endpoint")

        now = time.time()

        if ip not in self.request_log:
            self.request_log[ip] = []

        self.request_log[ip].append((endpoint, now))

        # remove old entries
        self.request_log[ip] = [
            entry for entry in self.request_log[ip]
            if now - entry[1] <= self.window
        ]

        count = len(self.request_log[ip])

        if count >= self.threshold:

            return {
                "enumeration": True,
                "count": count
            }

        return {
            "enumeration": False,
            "count": count
        }