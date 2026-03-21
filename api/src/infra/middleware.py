import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from sqlalchemy.orm import joinedload
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.auth_dependency import hash_token
from src.db.session import SessionLocal
from src.models import Session, User

from .request_context import RequestContext, set_context

API_VENDOR = "restaurant-api"


def get_user_token_from_header(auth_header: str | None) -> str | None:
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    return auth_header.replace("Bearer ", "").strip()


CallType = Callable[[Request], Awaitable[Response]]


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: CallType) -> Response:
        auth_header = request.headers.get("Authorization")
        token = get_user_token_from_header(auth_header)
        username = None
        if token:
            db = SessionLocal()
            try:
                session = (
                    db.query(Session)
                    .options(joinedload(Session.user))
                    .filter(Session.session == hash_token(token))
                    .first()
                )
                if session and session.user and session.user.is_active:
                    username = session.user.username
            except Exception:
                pass
            finally:
                db.close()

        version_app = request.headers.get("X-App-Version", "0.0.0")
        ctx = RequestContext(
            user_token=token, username=username, version_app=version_app
        )
        set_context(ctx)

        response = await call_next(request)
        return response


logger = logging.getLogger("request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: CallType):
        start = time.perf_counter()

        response = await call_next(request)

        duration = (time.perf_counter() - start) * 1000

        logger.info(
            "[%s %s] -> %s (%.2fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response
