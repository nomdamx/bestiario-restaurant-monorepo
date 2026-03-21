import logging
import sys

from src.config import get_config

from .request_context import get_context


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        ctx = get_context()

        record.session_hash = "-"
        record.username = "-"
        record.version_app = "-"

        if ctx:
            record.session_hash = str(ctx.user_token)[:5]
            record.username = str(ctx.username)
            record.version_app = str(ctx.version_app)

        return True


CONFIG = get_config()


def setup_request_logger():
    logger = logging.getLogger("request")

    level_debug = logging.DEBUG if CONFIG.DEBUG else logging.INFO

    logger.setLevel(level_debug)
    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "[%(levelname)s] [request] "
        "[version_app:%(version_app)s] "
        "[session:%(session_hash)s] "
        "[username:%(username)s] "
        "%(message)s"
    )

    handler.addFilter(ContextFilter())
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


def setup_socket_logger():
    socket_logger = logging.getLogger("socket")
    level_debug = logging.DEBUG if CONFIG.DEBUG else logging.INFO
    socket_logger.setLevel(level_debug)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter("[%(levelname)s] [Ticket Watcher] %(message)s")

    handler.setFormatter(formatter)

    socket_logger.addHandler(handler)
    socket_logger.propagate = False

    return socket_logger


def setup_error_logger():
    error_logger = logging.getLogger("error")
    error_logger.setLevel(logging.ERROR)

    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        "[%(levelname)s] [request] "
        "[version_app:%(version_app)s] "
        "[session:%(session_hash)s] "
        "[username:%(username)s] "
        "%(message)s"
    )
    handler.addFilter(ContextFilter())
    handler.setFormatter(formatter)

    error_logger.addHandler(handler)
    error_logger.propagate = False

    return error_logger
