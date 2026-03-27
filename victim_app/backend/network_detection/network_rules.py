from collections import defaultdict
import time


class NetworkRuleEngine:

    def __init__(self):

        self.connection_log = defaultdict(list)
        self.port_activity = defaultdict(set)

    # ---------------------------------
    # Port Scan Detection
    # ---------------------------------

    def detect_port_scan(self, ip, port):

        self.port_activity[ip].add(port)

        if len(self.port_activity[ip]) > 10:

            return {
                "attack": "Port Scan",
                "ip": ip,
                "severity": "HIGH"
            }

        return None


    # ---------------------------------
    # Brute Force Detection
    # ---------------------------------

    def detect_bruteforce(self, ip):

        now = time.time()

        self.connection_log[ip].append(now)

        recent = [
            t for t in self.connection_log[ip]
            if now - t < 30
        ]

        if len(recent) > 20:

            return {
                "attack": "Network Brute Force",
                "ip": ip,
                "severity": "HIGH"
            }

        return None


    # ---------------------------------
    # Request Burst Detection
    # ---------------------------------

    def detect_request_burst(self, ip):

        now = time.time()

        self.connection_log[ip].append(now)

        recent = [
            t for t in self.connection_log[ip]
            if now - t < 10
        ]

        if len(recent) > 50:

            return {
                "attack": "Request Burst",
                "ip": ip,
                "severity": "MEDIUM"
            }

        return None