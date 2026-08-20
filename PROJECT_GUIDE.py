"""
MERIDIAN PIVOT - PYTHON-ONLY PROJECT GUIDE
==========================================

Purpose
-------
This project implements the two-stage assignment:

1. Assignment 1 / Evaluation Phase:
   - learn an unfamiliar synchronization concept;
   - build a mini prototype;
   - original Northstar requirement: poll warehouse stock every 5 minutes,
     cache stock, expose a query endpoint;
   - keep a learning/blocker journal.

2. Pivot:
   - the polling approach is obsolete;
   - final requirement becomes Solstice Events check-in;
   - QR scan -> publish print request -> PENDING;
   - printer completion -> webhook -> CHECKED_IN;
   - duplicate scans are blocked;
   - callbacks can arrive out of order;
   - obsolete polling code is marked DEPRECATED and is not running.

Python-only rule
----------------
The implementation uses Python and only Python's standard library.
No Flask, JavaScript, HTML, CSS, Node.js, Go, or external package is required.

Run Assignment 1 demo
---------------------
python inventory_demo.py

Run the pivot demo
------------------
python demo_pivot.py

Run tests
----------
python tests.py

Run the final service
---------------------
python main.py

HTTP examples
-------------
POST /checkin
JSON:
{"attendee_id":"A001"}

GET /status/A001

POST /webhook/print-complete
The request must contain X-Webhook-Signature.
The demo uses webhook.sign_payload(payload) to create the signature.

Architecture
------------
Client/Kiosk
    |
    | QR scan
    v
CheckInService
    |
    | publish
    v
Python PrintRequestQueue
    |
    v
BadgePrinterVendor / real vendor queue adapter
    |
    | callback
    v
Webhook verification
    |
    v
CheckInService
    |
    v
CHECKED_IN

Important state rule
--------------------
A scan does NOT mean checked in.
The attendee remains PENDING until a verified successful webhook arrives.

Important pivot rule
--------------------
inventory_sync_original.py is deliberately marked DEPRECATED. It is
learning evidence for the original spec, not a parallel production path.
"""
