"""Asynchronous badge-printer vendor simulator.

It consumes messages from the Python queue and sends webhook callbacks.
Callbacks can be deliberately delivered out of order to test the pivot.
"""

import time
from threading import Thread

from webhook import sign_payload


class BadgePrinterVendor:
    def __init__(self, service):
        self.service = service

    def process_one(self, delay=0.2, success=True):
        message = self.service.queue.consume(timeout=1)
        if message is None:
            return False

        time.sleep(delay)

        payload = {
            "job_id": message["job_id"],
            "attendee_id": message["attendee_id"],
            "success": success,
        }
        signature = sign_payload(payload)

        # Direct Python call models the vendor HTTP POST to our webhook.
        self.service.handle_signed_webhook(payload, signature)
        self.service.queue.task_done()
        return True

    def process_all(self, delays=None):
        delays = delays or [0.2]
        threads = []

        for index, delay in enumerate(delays):
            thread = Thread(
                target=self.process_one,
                kwargs={"delay": delay, "success": True},
                daemon=True,
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
