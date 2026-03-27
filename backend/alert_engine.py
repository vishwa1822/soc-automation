from datetime import datetime


class AlertEngine:

    def __init__(self):
        pass

    # ------------------------------
    # Map numeric risk to severity
    # ------------------------------
    def calculate_severity(self, risk_score: int | float) -> str:

        if risk_score >= 80:
            return "CRITICAL"

        if risk_score >= 60:
            return "HIGH"

        if risk_score >= 40:
            return "MEDIUM"

        return "LOW"

    # ------------------------------
    # Create a single alert object
    # ------------------------------
    def generate_alert(
        self,
        log: dict,
        risk_score: int | float,
        severity: str | None = None,
        honeytoken_result: dict | None = None,
        enumeration_result: dict | None = None,
    ) -> dict:

        severity = severity or self.calculate_severity(risk_score)

        honeytoken_result = honeytoken_result or {}
        enumeration_result = enumeration_result or {}

        base = {
            "timestamp": datetime.utcnow().isoformat(),
            "ip": log.get("ip"),
            "username": log.get("username"),
            "endpoint": log.get("endpoint"),
            "risk_score": risk_score,
            "severity": severity,
        }

        # Add honeytoken context if triggered
        if honeytoken_result.get("triggered"):
            base["honeytoken"] = {
                "triggered": True,
                "endpoint": honeytoken_result.get("endpoint"),
                "attacker_ip": honeytoken_result.get("ip"),
            }

        # Add enumeration context if active
        if enumeration_result.get("enumeration"):
            base["enumeration"] = {
                "active": True,
                "count": enumeration_result.get("count"),
            }

        return base