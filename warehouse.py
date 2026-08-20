"""Python-only warehouse simulator for Assignment 1."""

from threading import Lock


class WarehouseSimulator:
    def __init__(self):
        self._stock = {
            "MILK-001": 12,
            "BREAD-001": 7,
            "RICE-001": 3,
            "SOAP-001": 20,
        }
        self._lock = Lock()

    def get_all_stock(self):
        with self._lock:
            return dict(self._stock)

    def update_stock(self, sku, quantity):
        with self._lock:
            self._stock[sku] = quantity
