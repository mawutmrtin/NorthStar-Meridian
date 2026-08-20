"""Webhook signing and verification using HMAC-SHA256."""

import hashlib
import hmac
import json


SECRET = b"meridian-demo-webhook-secret"


def canonical_json(payload: dict) -> bytes:
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sign_payload(payload: dict) -> str:
    return hmac.new(
        SECRET, canonical_json(payload), hashlib.sha256
    ).hexdigest()


def verify_signature(payload: dict, signature: str) -> bool:
    expected = sign_payload(payload)
    return hmac.compare_digest(expected, signature)
