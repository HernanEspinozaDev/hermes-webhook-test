# hermes-webhook-test

A small local-only Python WSGI service used to exercise the Hermes Kanban → GitHub → CI → webhook review workflow.

## CI

[![CI](https://github.com/HernanEspinozaDev/hermes-webhook-test/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/HernanEspinozaDev/hermes-webhook-test/actions/workflows/ci.yml)

## Run locally

```bash
python -m pip install -e '.[dev]'
python -m hermes_webhook_test.app
```

The service binds only to `127.0.0.1:8765`. Check `http://127.0.0.1:8765/health` for its health response.

## Validate

```bash
ruff check .
pytest -q
python -m build
```

The original README edits used to test GitHub webhooks have been retained in the repository history.
