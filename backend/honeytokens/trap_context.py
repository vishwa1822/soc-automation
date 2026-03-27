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