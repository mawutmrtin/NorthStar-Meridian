"""Final pivoted Solstice Events check-in service."""

from dataclasses import asdict
from threading import Lock
from uuid import uuid4

from models import PrintJob
from message_queue import PrintRequestQueue


class CheckInService:
    def __init__(self):
        self.attendees = {
            "A001": {"name": "Amina", "status": "NOT_CHECKED_IN"},
            "A002": {"name": "Daniel", "status": "NOT_CHECKED_IN"},
            "A003": {"name": "Grace", "status": "NOT_CHECKED_IN"},
        }
        self.jobs = {}
        self.queue = PrintRequestQueue()
        self._lock = Lock()

    def scan(self, attendee_id: str) -> dict:
        """Accept a QR scan and publish exactly one print request.

        The attendee is NOT marked checked in until the webhook confirms
        successful printing.
        """
        with self._lock:
            attendee = self.attendees.get(attendee_id)
            if attendee is None:
                return {
                    "ok": False,
                    "status": "NOT_FOUND",
                    "message": "Attendee does not exist.",
                }

            if attendee["status"] == "CHECKED_IN":
                return {
                    "ok": False,
                    "status": "ALREADY_CHECKED_IN",
                    "message": "Duplicate scan blocked; no second badge is printed.",
                }

            if attendee["status"] == "PENDING":
                return {
                    "ok": True,
                    "status": "PENDING",
                    "message": "A print request is already pending.",
                }

            job_id = uuid4().hex
            job = PrintJob(job_id=job_id, attendee_id=attendee_id, status="pending")
            self.jobs[job_id] = job
            attendee["status"] = "PENDING"

            published = self.queue.publish({
                "job_id": job_id,
                "attendee_id": attendee_id,
            })

            if not published:
                attendee["status"] = "NOT_CHECKED_IN"
                del self.jobs[job_id]
                return {
                    "ok": False,
                    "status": "QUEUE_ERROR",
                    "message": "The print request could not be queued.",
                }

            return {
                "ok": True,
                "status": "PENDING",
                "job_id": job_id,
                "message": "Print request queued. Waiting for webhook confirmation.",
            }

    def handle_signed_webhook(self, payload: dict, signature: str) -> dict:
        from webhook import verify_signature
        if not verify_signature(payload, signature):
            return {"ok": False, "status": "INVALID_SIGNATURE"}
        return self.handle_webhook(payload)

    def handle_webhook(self, payload: dict) -> dict:
        """Apply completion callbacks safely and idempotently.

        A callback that arrives after a newer final state is ignored.
        """
        job_id = payload.get("job_id")
        success = payload.get("success")

        with self._lock:
            job = self.jobs.get(job_id)
            if job is None:
                return {"ok": False, "status": "UNKNOWN_JOB"}

            attendee = self.attendees[job.attendee_id]

            if job.status == "completed":
                return {
                    "ok": True,
                    "status": "ALREADY_COMPLETED",
                    "message": "Duplicate webhook ignored.",
                }

            if job.status == "failed":
                return {
                    "ok": True,
                    "status": "ALREADY_FAILED",
                    "message": "Late webhook ignored.",
                }

            if success is True:
                job.status = "completed"
                attendee["status"] = "CHECKED_IN"
                return {
                    "ok": True,
                    "status": "CHECKED_IN",
                    "attendee_id": job.attendee_id,
                    "job_id": job_id,
                }

            job.status = "failed"
            job.error = payload.get("error", "Printer reported failure.")
            attendee["status"] = "NOT_CHECKED_IN"
            return {
                "ok": True,
                "status": "PRINT_FAILED",
                "attendee_id": job.attendee_id,
                "job_id": job_id,
                "message": job.error,
            }

    def status(self, attendee_id: str) -> dict:
        with self._lock:
            attendee = self.attendees.get(attendee_id)
            if attendee is None:
                return {"ok": False, "status": "NOT_FOUND"}
            return {
                "ok": True,
                "attendee_id": attendee_id,
                "name": attendee["name"],
                "status": attendee["status"],
            }

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "attendees": dict(self.attendees),
                "jobs": {k: asdict(v) for k, v in self.jobs.items()},
            }
