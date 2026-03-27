from collections import defaultdict
import time


class FeatureEngineeringEngine:

    def __init__(self):

        self.user_requests = defaultdict(list)
        self.user_failed_logins = defaultdict(int)
        self.user_endpoints = defaultdict(set)
        self.user_ips = defaultdict(set)


    def extract(self, log):

        user = log.get("username", "unknown")
        ip = log.get("ip_address")
        endpoint = log.get("endpoint", "")
        login_status = log.get("login_status")

        timestamp = time.time()

        # track requests
        self.user_requests[user].append(timestamp)

        # track endpoints
        self.user_endpoints[user].add(endpoint)

        # track IP addresses
        if ip:
            self.user_ips[user].add(ip)

        # track failed logins
        if login_status == "failed":
            self.user_failed_logins[user] += 1


        # -----------------------------
        # Feature Calculations
        # -----------------------------

        one_minute = 60

        recent_requests = [
            t for t in self.user_requests[user]
            if timestamp - t < one_minute
        ]

        request_rate = len(recent_requests)

        failed_login_count = self.user_failed_logins[user]

        unique_endpoints = len(self.user_endpoints[user])

        unique_ip_count = len(self.user_ips[user])

        session_duration = request_rate

        resource_access_count = unique_endpoints

        login_attempts = failed_login_count


        # ratio calculation
        failed_login_ratio = 0

        if request_rate > 0:
            failed_login_ratio = failed_login_count / request_rate


        features = [

            request_rate,
            failed_login_count,
            failed_login_ratio,
            unique_endpoints,
            unique_ip_count,
            session_duration,
            resource_access_count,
            login_attempts

        ]

        return features