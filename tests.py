"""Regression tests for both the original learning prototype and pivot."""

import unittest

from checkin_service import CheckInService
from webhook import sign_payload, verify_signature
from warehouse import WarehouseSimulator
from inventory_sync_original import PollingInventoryPrototype


class InventoryPrototypeTests(unittest.TestCase):
    def test_poll_and_query(self):
        warehouse = WarehouseSimulator()
        service = PollingInventoryPrototype(warehouse)
        service.poll_once()
        self.assertEqual(service.query("MILK-001"), 12)


class PivotTests(unittest.TestCase):
    def setUp(self):
        self.service = CheckInService()

    def webhook(self, job):
        payload = {
            "job_id": job["job_id"],
            "attendee_id": self.service.jobs[job["job_id"]].attendee_id,
            "success": True,
        }
        signature = sign_payload(payload)
        self.assertTrue(verify_signature(payload, signature))
        return self.service.handle_webhook(payload)

    def test_three_attendees_and_duplicate(self):
        jobs = [self.service.scan(x) for x in ("A001", "A002", "A003")]
        self.assertTrue(all(j["status"] == "PENDING" for j in jobs))

        duplicate = self.service.scan("A001")
        self.assertEqual(duplicate["status"], "PENDING")

        for job in reversed(jobs):
            result = self.webhook(job)
            self.assertEqual(result["status"], "CHECKED_IN")

        duplicate_after = self.service.scan("A001")
        self.assertEqual(duplicate_after["status"], "ALREADY_CHECKED_IN")

    def test_duplicate_webhook_is_idempotent(self):
        job = self.service.scan("A001")
        first = self.webhook(job)
        second = self.webhook(job)
        self.assertEqual(first["status"], "CHECKED_IN")
        self.assertEqual(second["status"], "ALREADY_COMPLETED")

    def test_bad_signature_is_rejected(self):
        payload = {"job_id": "fake", "attendee_id": "A001", "success": True}
        self.assertFalse(verify_signature(payload, "wrong-signature"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
