from honeytokens.engine_instance import honeytoken_engine
from network_detection.enumeration_detector import EnumerationDetector

from alert_store import record_alert
from riskengine import RiskEngine
from alert_engine import AlertEngine
from timeline_engine import TimelineEngine
from investigation_engine import InvestigationEngine


class LogProcessor:

    def __init__(self):

        # Detection Engines
        self.honeytoken_engine = honeytoken_engine
        self.enumeration_detector = EnumerationDetector()

        # SOC Analysis Engines
        self.risk_engine = RiskEngine()
        self.alert_engine = AlertEngine()
        self.timeline_engine = TimelineEngine()
        self.investigation_engine = InvestigationEngine()

    def process_log(self, log: dict):

        results: dict = {}

        # -----------------------------
        # Enumeration Detection (recon first)
        # -----------------------------
        enumeration_result = self.enumeration_detector.detect(log)
        results["enumeration"] = enumeration_result

        # -----------------------------
        # Honeytoken Detection
        # -----------------------------
        honeytoken_result = self.honeytoken_engine.detect(log)
        results["honeytoken"] = honeytoken_result

        # -----------------------------
        # Risk Calculation
        # -----------------------------
        risk_result = self.risk_engine.calculate_risk(
            honeytoken_result=honeytoken_result,
            enumeration_result=enumeration_result,
        )

        results["risk"] = risk_result

        # -----------------------------
        # Alert Generation
        # -----------------------------
        alert = self.alert_engine.generate_alert(
            log,
            risk_result.get("risk_score", 0),
            risk_result.get("severity"),
            honeytoken_result=honeytoken_result,
            enumeration_result=enumeration_result,
        )

        results["alert"] = alert

        record_alert(alert)

        # -----------------------------
        # Timeline Tracking
        # -----------------------------
        self.timeline_engine.add_event(log)

        # -----------------------------
        # Investigation Analysis
        # -----------------------------
        investigation = self.investigation_engine.analyze(log, results)

        results["investigation"] = investigation

        return results