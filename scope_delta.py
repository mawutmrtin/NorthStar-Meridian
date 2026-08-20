"""Assignment 2 Scope Delta Analysis."""

SCOPE_DELTA = {
    "dropped": [
        "Five-minute polling as the production synchronization mechanism.",
        "Waiting synchronously for a printer success response.",
        "Immediate CHECKED_IN state after the scan button is pressed.",
    ],
    "modified": [
        "Stock-sync learning prototype was refocused into an event check-in service.",
        "Completion is now driven by webhook confirmation.",
        "Duplicate protection now covers pending and completed states.",
        "Webhook handling is idempotent so repeated callbacks do not repeat completion.",
    ],
    "added": [
        "Print request message queue.",
        "Webhook endpoint.",
        "HMAC webhook signature verification.",
        "Pending state.",
        "Out-of-order callback regression test.",
    ],
    "regression_checks": [
        "Three test attendees can be scanned.",
        "A duplicate scan does not create a second print job.",
        "Attendee remains PENDING until successful webhook.",
        "Webhook can complete jobs in a different order from scan order.",
        "Repeated webhook does not duplicate completion.",
        "Invalid webhook signature is rejected.",
        "Obsolete polling code is visibly marked DEPRECATED and is not started by the final service.",
    ],
}


def print_scope_delta():
    for section, items in SCOPE_DELTA.items():
        print(f"\n{section.upper()}")
        for item in items:
            print(f"- {item}")


if __name__ == "__main__":
    print_scope_delta()
