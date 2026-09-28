from __future__ import annotations

import json
import os
from wsgiref.simple_server import WSGIServer, make_server
from wsgiref.types import StartResponse, WSGIEnvironment

from hermes_webhook_test import __version__


def application(environ: WSGIEnvironment, start_response: StartResponse) -> list[bytes]:
    """Serve a small JSON health endpoint for local workflow/deploy checks."""
    path = str(environ.get("PATH_INFO", "/"))
    method = str(environ.get("REQUEST_METHOD", "GET")).upper()

    if path not in {"/health", "/version"}:
        status = "404 Not Found"
        payload = {"error": "not_found"}
    elif method != "GET":
        status = "405 Method Not Allowed"
        payload = {"error": "method_not_allowed"}
    elif path == "/version":
        status = "200 OK"
        payload = {"version": __version__}
    else:
        status = "200 OK"
        payload = {"status": "ok"}

    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    headers = [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(body))),
    ]
    if status == "405 Method Not Allowed":
        headers.append(("Allow", "GET"))
    start_response(status, headers)
    return [body]


def serve() -> None:
    """Run the service on loopback only; no public listener is created."""
    port = int(os.environ.get("PORT", "8765"))
    server: WSGIServer = make_server("127.0.0.1", port, application)
    with server:
        print(f"hermes-webhook-test listening on http://127.0.0.1:{port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    serve()
