import logging
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException) -> tuple[object, int]:
        return jsonify(error={"code": error.name, "message": error.description}), error.code or 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> tuple[object, int]:
        logger.exception("Unhandled application error")
        return jsonify(error={"code": "Internal Server Error", "message": "An unexpected error occurred."}), 500
