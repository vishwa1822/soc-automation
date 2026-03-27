class InvestigationEngine:

    def __init__(self):

        self.events = []

    def analyze(self, log, results):

        investigation = {
            "ip": log.get("ip"),
            "endpoint": log.get("endpoint"),
            "analysis": []
        }

        # honeytoken investigation
        if results.get("honeytoken", {}).get("triggered"):

            investigation["analysis"].append(
                "Dynamic honeytoken triggered – possible attacker probing hidden resources"
            )

        # enumeration investigation
        if results.get("enumeration", {}).get("enumeration"):

            investigation["analysis"].append(
                "Multiple endpoint access attempts detected – possible enumeration attack"
            )

        # anomaly investigation
        if results.get("ml_anomaly", {}).get("anomaly"):

            investigation["analysis"].append(
                "Machine learning anomaly detected in request behavior"
            )

        if not investigation["analysis"]:

            investigation["analysis"].append(
                "No suspicious activity detected"
            )

        self.events.append(investigation)

        return investigation