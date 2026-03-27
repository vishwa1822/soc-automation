from collections import defaultdict
from datetime import datetime
import math


class BehavioralDetectionEngine:

    def __init__(self):
        self.failed_logins = defaultdict(list)
        self.user_locations = defaultdict(list)
        self.mfa_attempts = defaultdict(int)

    # ------------------------------
    # Brute Force Detection
    # ------------------------------
    def detect_bruteforce(self, user_id, timestamp):

        self.failed_logins[user_id].append(timestamp)

        attempts = self.failed_logins[user_id]

        if len(attempts) >= 5:
            return {
                "alert": True,
                "attack_type": "Brute Force Attack",
                "risk": 70
            }

        return None

    # ------------------------------
    # Credential Stuffing Detection
    # ------------------------------
    def detect_credential_stuffing(self, ip_address, user_id):

        if ip_address.startswith("192.168"):

            return {
                "alert": True,
                "attack_type": "Credential Stuffing",
                "risk": 60
            }

        return None

    # ------------------------------
    # Impossible Travel Detection
    # ------------------------------
    def detect_impossible_travel(self, user_id, geo_location, timestamp):

        history = self.user_locations[user_id]

        history.append((geo_location, timestamp))

        if len(history) < 2:
            return None

        last_location, last_time = history[-2]

        if last_location != geo_location:

            return {
                "alert": True,
                "attack_type": "Impossible Travel",
                "risk": 80
            }

        return None

    # ------------------------------
    # MFA Abuse Detection
    # ------------------------------
    def detect_mfa_abuse(self, user_id):

        self.mfa_attempts[user_id] += 1

        if self.mfa_attempts[user_id] >= 3:

            return {
                "alert": True,
                "attack_type": "MFA Abuse",
                "risk": 65
            }

        return None

    # ------------------------------
    # Sensitive Resource Access
    # ------------------------------
    def detect_sensitive_access(self, sensitivity_level):

        if sensitivity_level in ["HIGH", "CRITICAL"]:

            return {
                "alert": True,
                "attack_type": "Sensitive Resource Access",
                "risk": 50
            }

        return None

    # ------------------------------
    # Main Detection Pipeline
    # ------------------------------
    def analyze_event(self, event):

        alerts = []

        if event.event_type == "login_failed":
            alert = self.detect_bruteforce(event.user_id, event.timestamp)
            if alert:
                alerts.append(alert)

        alert = self.detect_credential_stuffing(event.ip_address, event.user_id)
        if alert:
            alerts.append(alert)

        alert = self.detect_impossible_travel(
            event.user_id,
            event.geo_location,
            event.timestamp
        )
        if alert:
            alerts.append(alert)

        if event.mfa_status == "failed":
            alert = self.detect_mfa_abuse(event.user_id)
            if alert:
                alerts.append(alert)

        alert = self.detect_sensitive_access(event.sensitivity_level)
        if alert:
            alerts.append(alert)

        return alerts