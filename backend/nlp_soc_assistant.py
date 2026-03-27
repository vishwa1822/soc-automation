from investigation_engine import InvestigationEngine


class SOCNLPAssistant:

    def __init__(self):
        self.investigator = InvestigationEngine()

    # -------------------------------
    # Parse User Query
    # -------------------------------
    def interpret_query(self, query: str):

        query = query.lower()

        if "top risky users" in query:
            return "TOP_RISKY_USERS"

        if "suspicious ip" in query:
            return "SUSPICIOUS_IPS"

        if "sensitive resource" in query:
            return "SENSITIVE_ACCESS"

        return "UNKNOWN"


    # -------------------------------
    # Execute Investigation
    # -------------------------------
    def execute_query(self, db, query: str):

        intent = self.interpret_query(query)

        if intent == "TOP_RISKY_USERS":
            return self.investigator.get_top_risky_users(db)

        if intent == "SUSPICIOUS_IPS":
            return self.investigator.get_suspicious_ips(db)

        if intent == "SENSITIVE_ACCESS":
            return self.investigator.get_sensitive_access_events(db)

        return {
            "message": "Query not understood"
        }