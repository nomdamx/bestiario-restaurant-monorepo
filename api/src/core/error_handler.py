import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .api_response import APIResponse, Metadata, Pagination
from .custom_errors import AppError

logger = logging.getLogger("request")


async def app_error_handler(request: Request, exc: Exception):
    if not isinstance(exc, AppError):
        return JSONResponse(
            status_code=500,
            content={
                "data": [],
                "meta": {
                    "error": "INTERNAL_SERVER_ERROR",
                    "message": "Unexpected error",
                },
            },
        )
    logger.info("[ERROR] -> %s", str(exc.message))
    logger.info("[ERROR] -> %s", str(exc.details))
    logger.info("[ERROR] -> %s", str(exc.error))

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": [],
            "meta": {
                "error": exc.error,
                "message": exc.message,
                "details": exc.details,
                **exc.extra,
            },
        },
    )


async def request_validation_handler(request: Request, exc: Exception):
    if not isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=500,
            content={
                "data": [],
                "meta": {
                    "error": "INTERNAL_SERVER_ERROR",
                    "message": "Unexpected validation error",
                },
            },
        )

    return JSONResponse(
        status_code=422,
        content={
            "data": [],
            "meta": {
                "error": "REQUEST_VALIDATION_ERROR",
                "details": exc.errors(),
            },
        },
    )
