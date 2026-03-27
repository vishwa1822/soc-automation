class RiskEngine:

    def __init__(self):

        self.weights = {
            "honeytoken": 50,
            "enumeration": 20,
            "ml_anomaly": 15,
            "behavior": 10,
            "correlation": 15
        }

    def calculate_risk(self,
                       ml_result=None,
                       behavior_result=None,
                       correlation_result=None,
                       honeytoken_result=None,
                       enumeration_result=None):

        # ensure dictionaries
        ml_result = ml_result or {}
        behavior_result = behavior_result or {}
        correlation_result = correlation_result or {}
        honeytoken_result = honeytoken_result or {}
        enumeration_result = enumeration_result or {}

        risk_score = 0
        risk_factors = []

        # Honeytoken detection
        if honeytoken_result.get("triggered"):

            risk_score += self.weights["honeytoken"]

            risk_factors.append({
                "type": "honeytoken_trigger",
                "endpoint": honeytoken_result.get("endpoint")
            })

        # Enumeration detection
        if enumeration_result.get("enumeration"):

            risk_score += self.weights["enumeration"]

            risk_factors.append({
                "type": "endpoint_enumeration",
                "count": enumeration_result.get("count", 0)
            })

        # ML anomaly
        if ml_result.get("anomaly"):

            risk_score += self.weights["ml_anomaly"]

            risk_factors.append({
                "type": "ml_anomaly"
            })

        # Behavioral anomaly
        if behavior_result.get("suspicious"):

            risk_score += self.weights["behavior"]

            risk_factors.append({
                "type": "behavior_anomaly"
            })

        # Correlation detection
        if correlation_result.get("attack_pattern"):

            risk_score += self.weights["correlation"]

            risk_factors.append({
                "type": "attack_correlation"
            })

        # Limit score
        risk_score = min(risk_score, 100)

        severity = self.get_severity(risk_score)

        return {
            "risk_score": risk_score,
            "severity": severity,
            "risk_factors": risk_factors
        }

    def get_severity(self, score):

        if score >= 80:
            return "critical"

        if score >= 60:
            return "high"

        if score >= 40:
            return "medium"

        return "low"