from flask import Blueprint, jsonify
from app.ports.inbound.health import HealthQuery


def create_health_blueprint(health_query: HealthQuery) -> Blueprint:
    blueprint = Blueprint("health", __name__)

    @blueprint.get("/health")
    def health() -> tuple[object, int]:
        result = health_query.execute()
        timestamp = result.timestamp.isoformat(timespec="microseconds").replace("+00:00", "Z")
        return jsonify(status=result.status, timestamp=timestamp), 200

    return blueprint
