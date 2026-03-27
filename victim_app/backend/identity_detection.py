import time
from collections import defaultdict


class IdentityDetectionEngine:

    def __init__(self):

        # store failed login timestamps
        self.failed_attempts = defaultdict(list)

        # detection settings
        self.threshold = 5
        self.time_window = 60


    def analyze_event(self, log):

        alerts = []

        username = log.get("username")
        ip = log.get("ip_address")
        login_status = log.get("login_status")

        if not username:
            return alerts

        current_time = time.time()

        if login_status == "failed":

            self.failed_attempts[username].append(current_time)

            # keep only recent attempts
            recent_attempts = [
                t for t in self.failed_attempts[username]
                if current_time - t < self.time_window
            ]

            self.failed_attempts[username] = recent_attempts

            if len(recent_attempts) >= self.threshold:

                alerts.append({
                    "alert_type": "Identity Brute Force",
                    "severity": "HIGH",
                    "username": username,
                    "ip_address": ip,
                    "attempts": len(recent_attempts)
                })

        return alerts
