from flask import Flask, Response

from .errors import NotFoundError, MethodNotAllowedError
from .base_resource import error_to_response
from .resources import actors_api, movies_api


def not_found_error(_) -> Response:
    """
    Custom 404 response.
    """
    error = NotFoundError()
    return error_to_response(error)


def not_allowed_error(_) -> Response:
    """
    Custom 405 response.
    """
    error = MethodNotAllowedError()
    return error_to_response(error)


def create_app() -> Flask:
    """
    Main application configuration
    """
    app = Flask(__name__)
    app.register_blueprint(actors_api)
    app.register_blueprint(movies_api)
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(405, not_allowed_error)
    return app
