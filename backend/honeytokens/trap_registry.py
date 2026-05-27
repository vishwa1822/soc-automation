import threading


class TrapRegistry:

    def __init__(self):

        self._lock = threading.Lock()
        self.active_traps = []

    def update_traps(self, traps):

        with self._lock:
            self.active_traps = list(traps)

    def is_trap(self, endpoint):

        with self._lock:
            return endpoint in self.active_traps

    def get_active_traps(self):

        with self._lock:
            return list(self.active_traps)

    def get_endpoint_traps(self):
        """URL paths registered as honeytoken endpoints (used by victim app sync)."""

        return self.get_active_traps()