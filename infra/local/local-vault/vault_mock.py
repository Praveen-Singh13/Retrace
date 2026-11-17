"""Local-only, in-memory secret service for the Compose development network."""

from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit

_secrets: dict[str, str] = {}
_name_pattern = re.compile(r"^[A-Za-z0-9-]{1,127}$")


class VaultHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/health":
            self._send(200, {"status": "ok"})
            return

        name = self._secret_name(path)
        if name is None:
            self._send(404, {"error": "not_found"})
        elif name not in _secrets:
            self._send(404, {"error": "secret_not_found"})
        else:
            self._send(200, {"name": name, "value": _secrets[name]})

    def do_PUT(self) -> None:
        name = self._secret_name(urlsplit(self.path).path)
        if name is None:
            self._send(404, {"error": "not_found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 1_048_576:
                raise ValueError
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self._send(400, {"error": "invalid_json"})
            return

        value = payload.get("value") if isinstance(payload, dict) else None
        if not isinstance(value, str):
            self._send(400, {"error": "value_must_be_string"})
            return

        _secrets[name] = value
        self._send(200, {"name": name})

    def do_DELETE(self) -> None:
        name = self._secret_name(urlsplit(self.path).path)
        if name is None:
            self._send(404, {"error": "not_found"})
        else:
            _secrets.pop(name, None)
            self._send(204)

    def log_message(self, _format: str, *_args: object) -> None:
        # Request logs can contain secret names or values; keep this fake silent.
        return

    @staticmethod
    def _secret_name(path: str) -> str | None:
        prefix = "/secrets/"
        if not path.startswith(prefix):
            return None
        name = unquote(path[len(prefix) :])
        return name if _name_pattern.fullmatch(name) else None

    def _send(self, status: int, payload: dict[str, str] | None = None) -> None:
        body = b"" if payload is None else json.dumps(payload).encode("utf-8")
        self.send_response(status)
        if payload is not None:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8200), VaultHandler).serve_forever()
