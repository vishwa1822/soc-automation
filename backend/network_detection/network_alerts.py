class NetworkAlertEngine:

    def generate_alerts(self, detections):

        alerts = []

        for d in detections:

            alert = {
                "alert_type": d["attack"],
                "source_ip": d["ip"],
                "severity": d["severity"]
            }

            alerts.append(alert)

        return alerts