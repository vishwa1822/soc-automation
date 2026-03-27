

from honeytokens.rotation_scheduler import RotationScheduler
from honeytokens.trap_registry import TrapRegistry
from honeytokens.trap_context import TrapContextTracker


class HoneytokenEngine:

    def __init__(self, registry: TrapRegistry | None = None):

        # store active traps (shared registry if provided)
        self.registry = registry or TrapRegistry()

        # track triggers for dashboard / investigation
        self.context_tracker = TrapContextTracker()

        # rotate traps every 3 minutes
        self.scheduler = RotationScheduler(
            self.registry,
            interval=180
        )

        # start rotation automatically so traps exist from startup
        self.scheduler.start()

    def detect(self, log):

        endpoint = log.get("endpoint")
        ip = log.get("ip")

        if self.registry.is_trap(endpoint):

            self.context_tracker.record_trigger(endpoint, ip)

            return {
                "triggered": True,
                "endpoint": endpoint,
                "ip": ip,
            }

        return {
            "triggered": False
        }

    def get_active_traps(self):

        return self.registry.get_active_traps()

    def get_trigger_history(self):

        return self.context_tracker.get_triggers()
       