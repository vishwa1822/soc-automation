from collections import defaultdict
import threading


class SOCMemoryStore:

    def __init__(self):

        self.lock = threading.Lock()

        # -----------------------------
        # Alert storage
        # -----------------------------
        self.alerts = []

        # -----------------------------
        # User activity memory
        # -----------------------------
        self.user_requests = defaultdict(list)
        self.user_failed_logins = defaultdict(int)
        self.user_endpoints = defaultdict(set)
        self.user_ips = defaultdict(set)

        # -----------------------------
        # Timeline storage
        # -----------------------------
        self.timelines = defaultdict(list)

        # -----------------------------
        # Batch investigation results
        # -----------------------------
        self.batch_results = []


    # -----------------------------
    # Alert Management
    # -----------------------------

    def add_alert(self, alert):

        with self.lock:

            self.alerts.append(alert)


    def get_alerts(self):

        return self.alerts


    # -----------------------------
    # Timeline Management
    # -----------------------------

    def add_timeline_event(self, user, event):

        with self.lock:

            self.timelines[user].append(event)


    def get_timeline(self, user):

        return self.timelines.get(user, [])


    # -----------------------------
    # Batch Results
    # -----------------------------

    def add_batch_result(self, result):

        with self.lock:

            self.batch_results.append(result)


    def get_batch_results(self):

        return self.batch_results