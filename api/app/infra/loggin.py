import logging
import sys
from app.infra.request_context import get_context
from flask import request, g
import time

class RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        ctx = get_context()

        record.user_id = "-"
        record.version_api = "-"
        record.username = "-"

        if ctx:
            if ctx.user:
                record.user_id = ctx.user.id
                record.username = ctx.user.username
            if ctx.version_api:
                record.version_api = ctx.version_api

        return True


def setup_request_logger():
    logger = logging.getLogger("request")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "[%(levelname)s] "
        "[request] "
        "[id_user:%(user_id)s] "
        "[username:%(username)s] "
        "[v:%(version_api)s] "
        "%(message)s"
    )

    handler.setFormatter(formatter)
    handler.addFilter(RequestContextFilter())

    logger.addHandler(handler)
    logger.propagate = False

    return logger

def log_request_start():
    g._request_start_time = time.perf_counter()


logger = logging.getLogger("request")
def log_request_end(response):
    try:
        start = getattr(g, "_request_start_time", None)
        duration_ms = (
            (time.perf_counter() - start) * 1000
            if start
            else -1
        )

        logger.info(
            "[%s %s] → %s (%.2fms)",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
        )

    except Exception:
        logger.exception("Error while logging request")

    return response

def setup_error_logger():
    error_logger = logging.getLogger("error")
    error_logger.setLevel(logging.ERROR)

    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        "[%(levelname)s] "
        "[request] "
        "[id_user:%(user_id)s] "
        "[username:%(username)s] "
        "[v:%(version_api)s] "
        "%(message)s"
    )
    handler.setFormatter(formatter)
    handler.addFilter(RequestContextFilter())

    error_logger.addHandler(handler)
    error_logger.propagate = False

    return error_logger

def setupt_socket_loggin():
    socket_logger = logging.getLogger("socket")
    socket_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(levelname)s] "
        "[Ticket Watcher] "
        "%(message)s"
    )
    handler.setFormatter(formatter)

    socket_logger.addHandler(handler)
    socket_logger.propagate = False

    return socket_logger