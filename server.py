"""Python standard-library HTTP server for the final pivoted service.

No Flask, JavaScript, HTML, or other programming language is required.
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from config import HOST, PORT
from checkin_service import CheckInService
from webhook import verify_signature


service = CheckInService()


class Handler(BaseHTTPRequestHandler):
    def _send(self, status_code, payload):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8")) if raw else {}

    def do_GET(self):
        if self.path.startswith("/status/"):
            attendee_id = self.path.rsplit("/", 1)[-1]
            self._send(200, service.status(attendee_id))
            return

        if self.path == "/":
            self._send(200, {
                "service": "Solstice Events Check-In Kiosk",
                "status": "running",
                "endpoints": [
                    "POST /checkin",
                    "POST /webhook/print-complete",
                    "GET /status/<attendee_id>",
                ],
                "note": "Checked in means printing has been confirmed by webhook.",
            })
            return

        self._send(404, {"error": "Not found"})

    def do_POST(self):
        try:
            payload = self._read_json()
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send(400, {"error": "Invalid JSON"})
            return

        if self.path == "/checkin":
            result = service.scan(payload.get("attendee_id", ""))
            self._send(200 if result.get("ok") else 400, result)
            return

        if self.path == "/webhook/print-complete":
            signature = self.headers.get("X-Webhook-Signature", "")
            if not verify_signature(payload, signature):
                self._send(401, {"ok": False, "status": "INVALID_SIGNATURE"})
                return

            result = service.handle_webhook(payload)
            self._send(200, result)
            return

        self._send(404, {"error": "Not found"})


def run():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Solstice Python check-in service: http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
