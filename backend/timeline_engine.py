from collections import defaultdict


class TimelineEngine:

    def __init__(self):
        self.sessions = defaultdict(list)

    def add_event(self, log):
        """
        Add log event to a session timeline
        """

        user = log.get("username", "unknown")
        timestamp = log.get("timestamp")

        event = {
            "timestamp": timestamp,
            "event": log.get("event"),
            "ip": log.get("ip")
        }

        self.sessions[user].append(event)

    def get_timeline(self, user):
        """
        Return ordered timeline for a user
        """

        events = self.sessions.get(user, [])

        sorted_events = sorted(
            events,
            key=lambda x: x["timestamp"]
        )

        return sorted_events

    def reconstruct_attack_chain(self, user):
        """
        Detect attack patterns from timeline
        """

        timeline = self.get_timeline(user)

        attack_chain = []

        for event in timeline:

            if event["event"] == "failed_login":
                attack_chain.append("Brute force attempt")

            elif event["event"] == "successful_login":
                attack_chain.append("Account compromise")

            elif event["event"] == "privilege_change":
                attack_chain.append("Privilege escalation")

            elif event["event"] == "file_download":
                attack_chain.append("Possible data exfiltration")

        return attack_chain