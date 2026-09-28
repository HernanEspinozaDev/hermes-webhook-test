from __future__ import annotations

import io
import json

from hermes_webhook_test import __version__
from hermes_webhook_test.app import application


def test_health_endpoint_returns_json_ok() -> None:
    response: dict[str, object] = {}

    def start_response(status: str, headers: list[tuple[str, str]]) -> None:
        response["status"] = status
        response["headers"] = headers

    body = b"".join(
        application(
            {"REQUEST_METHOD": "GET", "PATH_INFO": "/health", "wsgi.input": io.BytesIO()},
            start_response,
        )
    )

    assert response["status"] == "200 OK"
    assert json.loads(body) == {"status": "ok"}


def test_version_endpoint_returns_package_version() -> None:
    response: dict[str, object] = {}

    def start_response(status: str, headers: list[tuple[str, str]]) -> None:
        response["status"] = status

    body = b"".join(
        application(
            {"REQUEST_METHOD": "GET", "PATH_INFO": "/version", "wsgi.input": io.BytesIO()},
            start_response,
        )
    )

    assert response["status"] == "200 OK"
    assert json.loads(body) == {"version": __version__}


def test_unknown_path_returns_not_found() -> None:
    response: dict[str, object] = {}

    def start_response(status: str, headers: list[tuple[str, str]]) -> None:
        response["status"] = status

    body = b"".join(
        application(
            {"REQUEST_METHOD": "GET", "PATH_INFO": "/missing", "wsgi.input": io.BytesIO()},
            start_response,
        )
    )

    assert response["status"] == "404 Not Found"
    assert json.loads(body) == {"error": "not_found"}


def test_health_endpoint_rejects_non_get_methods() -> None:
    response: dict[str, object] = {}
    response_headers: list[tuple[str, str]] = []

    def start_response(status: str, headers: list[tuple[str, str]]) -> None:
        response["status"] = status
        response_headers.extend(headers)

    body = b"".join(
        application(
            {"REQUEST_METHOD": "POST", "PATH_INFO": "/health", "wsgi.input": io.BytesIO()},
            start_response,
        )
    )

    assert response["status"] == "405 Method Not Allowed"
    assert ("Allow", "GET") in response_headers
    assert json.loads(body) == {"error": "method_not_allowed"}


def test_version_endpoint_rejects_non_get_methods() -> None:
    response: dict[str, object] = {}
    response_headers: list[tuple[str, str]] = []

    def start_response(status: str, headers: list[tuple[str, str]]) -> None:
        response["status"] = status
        response_headers.extend(headers)

    body = b"".join(
        application(
            {"REQUEST_METHOD": "POST", "PATH_INFO": "/version", "wsgi.input": io.BytesIO()},
            start_response,
        )
    )

    assert response["status"] == "405 Method Not Allowed"
    assert ("Allow", "GET") in response_headers
    assert json.loads(body) == {"error": "method_not_allowed"}
