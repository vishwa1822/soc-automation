from collections import defaultdict


class AttackCorrelationEngine:

    def __init__(self):

        # Store user activity timelines
        self.user_activity = defaultdict(list)

    # --------------------------------
    # Add event to timeline
    # --------------------------------
    def add_event(self, log):

        user = log.user_id

        event = {
            "timestamp": log.timestamp,
            "event_type": log.event_type,
            "ip": log.ip_address,
            "resource": log.resource_accessed
        }

        self.user_activity[user].append(event)

    # --------------------------------
    # Detect multi-stage attack
    # --------------------------------
    def detect_attack_chain(self, user):

        events = self.user_activity[user]

        if len(events) < 3:
            return None

        attack_chain = []

        for e in events:
            attack_chain.append(e["event_type"])

        # Example detection logic
        if (
            "login_failed" in attack_chain and
            "login_success" in attack_chain and
            "resource_access" in attack_chain
        ):

            return {
                "attack_detected": True,
                "attack_type": "Account Compromise",
                "timeline": events
            }

        return None

    # --------------------------------
    # Process new event
    # --------------------------------
    def process_event(self, log):

        self.add_event(log)

        attack = self.detect_attack_chain(log.user_id)

        return attack