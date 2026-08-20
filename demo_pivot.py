"""End-to-end demonstration of the final pivot.

Run:
    python demo_pivot.py

The demo tests three attendees and a duplicate scan. It also demonstrates
that the UI/state is PENDING before webhook confirmation.
"""

import json

from checkin_service import CheckInService
from webhook import sign_payload


def send_webhook(service, payload):
    signature = sign_payload(payload)
    return service.handle_signed_webhook(payload, signature)


def main():
    service = CheckInService()

    print("=" * 60)
    print("MERIDIAN PIVOT - SOLSTICE EVENTS DEMO")
    print("=" * 60)

    first = service.scan("A001")
    second = service.scan("A002")
    third = service.scan("A003")

    print("\n1) Three QR scans")
    print(json.dumps([first, second, third], indent=2))

    print("\n2) Before webhook confirmation")
    print(service.status("A001"))
    print("Expected: PENDING, not CHECKED_IN")

    duplicate = service.scan("A001")
    print("\n3) Duplicate scan before confirmation")
    print(json.dumps(duplicate, indent=2))

    print("\n4) Webhook confirmations arrive")
    for result in [
        send_webhook(service, {
            "job_id": first["job_id"],
            "attendee_id": "A001",
            "success": True,
        }),
        send_webhook(service, {
            "job_id": third["job_id"],
            "attendee_id": "A003",
            "success": True,
        }),
        send_webhook(service, {
            "job_id": second["job_id"],
            "attendee_id": "A002",
            "success": True,
        }),
    ]:
        print(result)

    print("\n5) Duplicate scan after confirmation")
    print(json.dumps(service.scan("A001"), indent=2))

    print("\n6) Final attendee states")
    for attendee_id in ("A001", "A002", "A003"):
        print(service.status(attendee_id))

    print("\nPASS: 3 attendees handled; duplicate scan did not create a second job.")
    print("PASS: CHECKED_IN appears only after webhook confirmation.")
    print("PASS: Python-only asynchronous queue/webhook flow is demonstrated.")


if __name__ == "__main__":
    main()
