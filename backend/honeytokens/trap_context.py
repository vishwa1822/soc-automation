import time
from collections import deque
from typing import Any, Deque, List


class TrapContext:

    def __init__(self):

        self.events = []

    def record(self, ip, action, resource):

        self.events.append({
            "ip": ip,
            "action": action,
            "resource": resource
        })

    def get_events(self):

        return self.events


class TrapContextTracker:
    """Records honeytoken trap hits for dashboards and SOAR history."""

    def __init__(self, maxlen: int = 200):
        self._triggers: Deque[dict[str, Any]] = deque(maxlen=maxlen)

    def record_trigger(self, endpoint: str, ip: str | None) -> None:
        self._triggers.append({
            "endpoint": endpoint or "",
            "ip": ip or "unknown",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        })

    def get_triggers(self) -> List[dict[str, Any]]:
        return list(self._triggers)