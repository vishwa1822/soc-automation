import asyncio
import inspect


class EventBus:
    def __init__(self, worker_count=3):
        self.subscribers = []
        self.queue = asyncio.Queue()
        self.worker_count = worker_count
        self.workers = []

    # Register detection engines
    def subscribe(self, handler):
        self.subscribers.append(handler)

    # Add event to queue
    async def publish(self, event):
        await self.queue.put(event)

    # Worker that processes events
    async def worker(self):
        while True:
            event = await self.queue.get()

            try:
                tasks = []

                for handler in self.subscribers:
                    # Support both async and sync handlers safely
                    if inspect.iscoroutinefunction(handler):
                        tasks.append(asyncio.create_task(handler(event)))
                    else:
                        # Run synchronous handlers in a thread so they don't block the loop
                        tasks.append(asyncio.create_task(asyncio.to_thread(handler, event)))

                if tasks:
                    await asyncio.gather(*tasks)

            except Exception as e:
                print(f"[EventBus Error] {e}")

            finally:
                self.queue.task_done()

    # Start workers
    async def start(self):
        for _ in range(self.worker_count):
            task = asyncio.create_task(self.worker())
            self.workers.append(task)

    # Stop workers
    async def stop(self):
        for worker in self.workers:
            worker.cancel()

        await asyncio.gather(*self.workers, return_exceptions=True)