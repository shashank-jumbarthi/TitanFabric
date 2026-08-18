from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from backend.catalog import estimate_quote, get_fabric, list_fabrics


def _json_response(handler: BaseHTTPRequestHandler, status: HTTPStatus, payload: Any) -> None:
    body = json.dumps(payload, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    lowered = value.lower()
    if lowered in {"1", "true", "yes"}:
        return True
    if lowered in {"0", "false", "no"}:
        return False
    raise ValueError("Boolean filters must be true or false")


def _validate_quote(payload: dict) -> None:
    if len(str(payload.get("customer_name", "")).strip()) < 2:
        raise ValueError("customer_name must be at least 2 characters")
    email = str(payload.get("email", ""))
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        raise ValueError("email must be valid")
    if payload.get("destination", "domestic") not in {"domestic", "international"}:
        raise ValueError("destination must be domestic or international")
    items = payload.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("items must contain at least one fabric")


class TitanFabricHandler(BaseHTTPRequestHandler):
    server_version = "TitanFabric/1.0"

    def do_OPTIONS(self) -> None:
        _json_response(self, HTTPStatus.NO_CONTENT, {})

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        try:
            if parsed.path == "/health":
                _json_response(self, HTTPStatus.OK, {"status": "ok", "service": "titanfabric"})
                return

            if parsed.path == "/fabrics":
                sustainable = _parse_bool(query.get("sustainable", [None])[0])
                max_price_value = query.get("max_price", [None])[0]
                max_price = float(max_price_value) if max_price_value else None
                category = query.get("category", [None])[0]
                _json_response(
                    self,
                    HTTPStatus.OK,
                    list_fabrics(category=category, sustainable=sustainable, max_price=max_price),
                )
                return

            if parsed.path.startswith("/fabrics/"):
                fabric_id = parsed.path.removeprefix("/fabrics/")
                fabric = get_fabric(fabric_id)
                if fabric is None:
                    _json_response(self, HTTPStatus.NOT_FOUND, {"detail": "Fabric not found"})
                    return
                _json_response(self, HTTPStatus.OK, fabric)
                return

            _json_response(self, HTTPStatus.NOT_FOUND, {"detail": "Not found"})
        except ValueError as exc:
            _json_response(self, HTTPStatus.BAD_REQUEST, {"detail": str(exc)})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/quotes":
            _json_response(self, HTTPStatus.NOT_FOUND, {"detail": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            _validate_quote(payload)
            estimate = estimate_quote(
                payload["items"],
                destination=payload.get("destination", "domestic"),
            )
            _json_response(
                self,
                HTTPStatus.OK,
                {
                    "status": "received",
                    "customer_name": payload["customer_name"],
                    "email": payload["email"],
                    "estimate": estimate,
                    "next_step": "A sourcing specialist will respond within one business day.",
                },
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            _json_response(self, HTTPStatus.BAD_REQUEST, {"detail": str(exc)})

    def log_message(self, format: str, *args: Any) -> None:
        return


def create_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), TitanFabricHandler)


def main() -> None:
    server = create_server()
    print("TitanFabric API running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
