"""A small Python-only message queue used to model the vendor queue.

It intentionally uses only the Python standard library. In production this
class could be replaced by a real vendor queue adapter without changing the
service logic.
"""

from queue import Queue, Empty
from threading import Lock


class PrintRequestQueue:
    def __init__(self):
        self._queue = Queue()
        self._seen = set()
        self._lock = Lock()

    def publish(self, message: dict) -> bool:
        job_id = message["job_id"]
        with self._lock:
            if job_id in self._seen:
                return False
            self._seen.add(job_id)
            self._queue.put(message)
            return True

    def consume(self, timeout=0.5):
        try:
            return self._queue.get(timeout=timeout)
        except Empty:
            return None

    def task_done(self):
        self._queue.task_done()
