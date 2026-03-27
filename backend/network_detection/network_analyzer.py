from network_rules import NetworkRuleEngine


class NetworkAnalyzer:

    def __init__(self):

        self.rules = NetworkRuleEngine()

    # ---------------------------------
    # Analyze network event
    # ---------------------------------

    def analyze_event(self, event):

        ip = event.get("ip")
        port = event.get("port")

        results = []

        port_scan = self.rules.detect_port_scan(ip, port)

        if port_scan:
            results.append(port_scan)

        brute_force = self.rules.detect_bruteforce(ip)

        if brute_force:
            results.append(brute_force)

        burst = self.rules.detect_request_burst(ip)

        if burst:
            results.append(burst)

        return results