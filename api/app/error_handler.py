from flask import Flask, request
from app.response_versions import get_version

from .custom_errors import (
    AppError,
    DatabaseError
)

from sqlalchemy.exc import (
    IntegrityError
)

import logging

logger_request = logging.getLogger("error")

def make_error_response(error:AppError):
    from flask import Response, json
    APIResponse = get_version()
    response = APIResponse(
        type = "error",
        error = error
    )

    logger_request.error(
        "[%s %s] %s: %s",
        request.method,
        request.path,
        error.error,
        error.details
    )

    return Response(
        response = json.dumps(response.get_error_response()),
        status = error.status_code,
        mimetype = "application/json"
    )

def register_error_handlers(app:Flask):

    @app.errorhandler(AppError)
    def handle_app_error(error:AppError):
        app.logger.error(f"{error.error}: {error.details}")
        logger_request.error(
            "[%s %s] %s: %s",
            request.method,
            request.path,
            error.error,
            error.details
        )
        return make_error_response(error)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        details = str(error.orig) if hasattr(error, "orig") else str(error)
        db_error =  DatabaseError(details=details, status_code=409)
        logger_request.error(
            "[%s %s] %s: %s",
            request.method,
            request.path,
            db_error.error,
            db_error.details
        )
        return make_error_response(db_error)
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        app_error = AppError(
            error="Unhandled Error",
            message="Something went wrong",
            details=str(error),
            status_code=500
        )
        logger_request.error(
            "[%s %s] %s: %s",
            request.method,
            request.path,
            app_error.error,
            app_error.details
        )
        return make_error_response(app_error)
    
    @app.errorhandler(TypeError)
    def handle_type_error(error):
        app_error = AppError(
            error="Type Error",
            message="Invalid type provided",
            details=str(error),
            status_code=400
        )
        logger_request.error(
            "[%s %s] %s: %s",
            request.method,
            request.path,
            app_error.error,
            app_error.details
        )
        return make_error_response(app_error)