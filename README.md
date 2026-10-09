# Flask Hexagonal REST API Boilerplate

A small, production-oriented Flask starter that keeps HTTP concerns in inbound adapters and business contracts in ports. The health use case is framework-independent.

## Architecture

```text
src/app/
├── adapters/          # Framework and infrastructure implementations
│   ├── inbound/http/  # Flask routes, errors, security middleware
│   └── outbound/      # Implementations of outbound ports
├── application/       # Use cases and orchestration
├── domain/            # Framework-free entities and value objects
├── ports/             # Inbound and outbound interfaces
├── config.py          # Environment-based configuration
└── bootstrap.py       # Dependency wiring / application factory
```

Dependency direction: adapters depend on ports/application/domain. The domain does not import Flask.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
flask --app app:create_app run
```

```bash
curl -i http://127.0.0.1:5000/api/v1/health
```

Example response:

```json
{"status":"healthy","timestamp":"2026-01-01T12:00:00.000000Z"}
```

## Docker

```bash
docker build -t flask-hexagonal-api .
docker run --rm -p 8000:8000 flask-hexagonal-api
```

Terminate TLS at a trusted reverse proxy/load balancer. Set `TRUST_PROXY=true` only when the app is behind a proxy you control. For multiple workers/instances, replace `memory://` with a shared rate-limit backend such as Redis.

## Security controls included

- Maximum request size, JSON-only POST/PUT/PATCH requests, global rate limit and generic errors.
- Security headers: HSTS on HTTPS, CSP, anti-sniffing, clickjacking protection, no-referrer, and restricted browser permissions.
- No secrets in source; configuration comes from environment variables.
- Non-root, slim container and production WSGI server.
- Request correlation ID with validation, without logging bodies, credentials, or tokens.
- `pip-audit`, Ruff security rules, tests, and CI dependency scanning.

This starter does not invent authentication or authorization. Add an identity-provider-backed mechanism and enforce object/function-level authorization in each protected use case before adding business endpoints. Never use Flask's development server in production.

## Quality checks

```bash
make lint test audit
```
