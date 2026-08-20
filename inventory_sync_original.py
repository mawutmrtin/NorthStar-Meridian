"""ASSIGNMENT 1 / ORIGINAL SPEC PROTOTYPE.

This is deliberately retained as a learning prototype. It models the
Day-3 requirement: poll a warehouse every five minutes, cache stock, and
answer stock queries.

The Day-4 pivot makes this approach obsolete. It is therefore NOT started by
the final application. It is kept here as visibly deprecated evidence.
"""

from dataclasses import dataclass
from threading import Lock
import time


@dataclass
class WarehouseItem:
    sku: str
    quantity: int


class PollingInventoryPrototype:
    DEPRECATED = True
    POLL_INTERVAL_SECONDS = 300  # five minutes

    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.cache = {}
        self._lock = Lock()

    def poll_once(self):
        """Deprecated: one synchronous warehouse poll."""
        data = self.warehouse.get_all_stock()
        with self._lock:
            self.cache = dict(data)
        return self.cache

    def run_forever(self):
        """Deprecated and intentionally not used by the pivoted system."""
        while True:
            self.poll_once()
            time.sleep(self.POLL_INTERVAL_SECONDS)

    def query(self, sku):
        with self._lock:
            return self.cache.get(sku)
