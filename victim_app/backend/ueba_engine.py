import numpy as np
from collections import defaultdict


class UEBAEngine:

    def __init__(self):

        # Store baseline behavior
        self.user_profiles = defaultdict(list)

    # --------------------------------
    # Build Behavior Profile
    # --------------------------------

    def build_profile(self, log):

        user = log.user_id

        behavior_vector = [

            getattr(log, "login_hour", 0),
            getattr(log, "failed_login_attempts", 0),
            getattr(log, "resource_access_count", 0),
            getattr(log, "device_count", 1)

        ]

        self.user_profiles[user].append(behavior_vector)

    # --------------------------------
    # Compute Baseline Behavior
    # --------------------------------

    def compute_baseline(self, user):

        data = np.array(self.user_profiles[user])

        if len(data) == 0:
            return None

        baseline = np.mean(data, axis=0)

        return baseline

    # --------------------------------
    # Detect Behavior Anomaly
    # --------------------------------

    def detect_anomaly(self, log):

        user = log.user_id

        baseline = self.compute_baseline(user)

        if baseline is None:
            return {"ueba_anomaly": False, "risk_score": 0}

        current = np.array([

            getattr(log, "login_hour", 0),
            getattr(log, "failed_login_attempts", 0),
            getattr(log, "resource_access_count", 0),
            getattr(log, "device_count", 1)

        ])

        distance = np.linalg.norm(current - baseline)

        if distance > 5:

            return {
                "ueba_anomaly": True,
                "risk_score": 85
            }

        return {
            "ueba_anomaly": False,
            "risk_score": 10
        }

    # --------------------------------
    # Main UEBA Analysis
    # --------------------------------

    def analyze(self, log):

        self.build_profile(log)

        return self.detect_anomaly(log)