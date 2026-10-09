import logging
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

from app.adapters.inbound.http.errors import register_error_handlers
from app.adapters.inbound.http.health_routes import create_health_blueprint
from app.adapters.inbound.http.security import register_security
from app.adapters.outbound.system_clock import SystemClock
from app.application.health_service import HealthService
from app.config import Settings


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()
    logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    app = Flask(__name__)
    app.config.update(
        MAX_CONTENT_LENGTH=settings.max_content_length,
        JSON_SORT_KEYS=False,
        PROPAGATE_EXCEPTIONS=False,
    )
    if settings.trust_proxy:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)  # type: ignore[method-assign]

    Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=[settings.rate_limit],
        storage_uri=settings.rate_limit_storage_uri,
        headers_enabled=True,
    )
    health_service = HealthService(SystemClock())
    app.register_blueprint(create_health_blueprint(health_service), url_prefix="/api/v1")
    register_security(app)
    register_error_handlers(app)
    return app
