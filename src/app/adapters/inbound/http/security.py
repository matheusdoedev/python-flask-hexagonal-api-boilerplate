import re
import uuid
from flask import Flask, abort, g, request

_REQUEST_ID = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


def register_security(app: Flask) -> None:
    @app.before_request
    def validate_request() -> None:
        supplied_id = request.headers.get("X-Request-ID", "")
        g.request_id = supplied_id if _REQUEST_ID.fullmatch(supplied_id) else str(uuid.uuid4())
        if request.method in {"POST", "PUT", "PATCH"} and not request.is_json:
            abort(415, description="Content-Type must be application/json.")

    @app.after_request
    def add_security_headers(response):  # type: ignore[no-untyped-def]
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Request-ID"] = g.get("request_id", str(uuid.uuid4()))
        if request.is_secure:
            response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        return response
