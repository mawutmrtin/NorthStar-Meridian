"""Run the complete demonstration and regression tests."""
import subprocess
import sys

print("\n=== ASSIGNMENT 1 DEMO ===")
subprocess.run([sys.executable, "inventory_demo.py"], check=True)

print("\n=== PIVOT DEMO ===")
subprocess.run([sys.executable, "demo_pivot.py"], check=True)

print("\n=== REGRESSION TESTS ===")
subprocess.run([sys.executable, "tests.py"], check=True)
