"""Run the Assignment 1 mini-prototype without waiting five minutes."""

from warehouse import WarehouseSimulator
from inventory_sync_original import PollingInventoryPrototype


def run_demo():
    warehouse = WarehouseSimulator()
    sync = PollingInventoryPrototype(warehouse)

    print("=== Assignment 1: Original Inventory Sync Prototype ===")
    print("Learning prototype: polling + cache + query")
    print("One poll is executed immediately for demonstration.")
    print()

    cache = sync.poll_once()
    for sku, quantity in cache.items():
        print(f"{sku}: {quantity} units")

    print()
    print("Query MILK-001:", sync.query("MILK-001"))
    print("NOTE: Continuous five-minute polling is deprecated after the pivot.")


if __name__ == "__main__":
    run_demo()
