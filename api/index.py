"""Public status function for Vercel.

This repo is a local CLI. The Vercel surface must boot without GoDaddy keys
and must never import godaddy_automation.py (that module exits if env is missing).
"""

from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        payload = {
            "service": "godaddy-secure-automation",
            "status": "ok",
            "surface": "public-status",
            "cli": "local-only",
            "secretsLoaded": False,
            "godaddyCalls": False,
            "note": "CLI stays on the owner host. This endpoint does not call GoDaddy.",
            "utc": datetime.now(timezone.utc).isoformat(),
        }
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return
