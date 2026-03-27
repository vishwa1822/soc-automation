class XAIAssistant:

    def explain_alert(self, analysis):

        explanation = []

        risk = analysis.get("risk_score", 0)

        if risk >= 80:
            explanation.append("High risk activity detected.")

        elif risk >= 50:
            explanation.append("Suspicious behaviour detected.")

        else:
            explanation.append("Low risk activity.")


        ml_result = analysis.get("ml_detection")

        if ml_result and ml_result.get("is_anomaly"):

            score = ml_result.get("anomaly_score")

            explanation.append(
                f"Machine learning model detected abnormal behaviour (score: {score})."
            )


        identity_alerts = analysis.get("identity_alerts")

        if identity_alerts:

            explanation.append(
                "Multiple failed login attempts indicate possible brute-force attack."
            )


        network_alerts = analysis.get("network_alerts")

        if network_alerts:

            explanation.append(
                "Network activity patterns suggest suspicious traffic."
            )


        attack_chain = analysis.get("attack_chain")

        if attack_chain:

            explanation.append(
                f"Attack chain detected: {' → '.join(attack_chain)}."
            )


        return " ".join(explanation)