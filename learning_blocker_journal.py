"""Assignment 1 Learning & Blocker Journal.

This is a Python data file so the project remains Python-only.
Edit the entries with your actual timestamps and personal learning evidence.
"""

JOURNAL = [
    {
        "day": "Day 1",
        "topic": "Message queue",
        "goal": "Understand publish/consume and duplicate message protection.",
        "blocker": "Initially unclear how queue consumers should acknowledge work.",
        "fix": "Built a small standard-library Queue prototype and used task_done().",
        "evidence": "message_queue.py",
    },
    {
        "day": "Day 1",
        "topic": "Webhook verification",
        "goal": "Understand how a callback can be authenticated.",
        "blocker": "A webhook request can be forged if the receiver trusts the body alone.",
        "fix": "Used HMAC-SHA256 signatures and constant-time comparison.",
        "evidence": "webhook.py and tests.py",
    },
    {
        "day": "Day 2",
        "topic": "Asynchronous state",
        "goal": "Represent pending work separately from completed work.",
        "blocker": "The old synchronous design treated a successful scan as immediate completion.",
        "fix": "Introduced PENDING and CHECKED_IN states and moved completion to the webhook.",
        "evidence": "checkin_service.py and demo_pivot.py",
    },
]


def show_journal():
    for entry in JOURNAL:
        print(entry)


if __name__ == "__main__":
    show_journal()
