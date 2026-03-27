import threading
import time
from honeytokens.trap_generator import generate_traps


class RotationScheduler:

    def __init__(self, registry, interval=180):

        self.registry = registry
        self.interval = interval
        self.running = False

    def start(self):

        # Avoid starting multiple scheduler threads
        if self.running:
            return

        self.running = True

        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    def run(self):

        while self.running:

            traps = generate_traps()

            self.registry.update_traps(traps)

            time.sleep(self.interval)

    def stop(self):

        self.running = False