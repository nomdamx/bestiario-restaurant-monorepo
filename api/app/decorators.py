import json

from functools import wraps
from flask import request,Response

from app import db
from app.models import (
    User
)
from app.models import Session
from app.infra import get_context
from hashlib import sha256

session = db.session

def requires_auth(auth_levels: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ctx = get_context()
            userSessionId = sha256(ctx.user_token.encode('utf-8'),usedforsecurity=True).hexdigest()
            query_user_session = session.query(Session).filter_by(session = userSessionId).first()
            
            if query_user_session is None:
                return Response(status=401)

            user = session.query(User).filter_by(
                id=query_user_session.id_user
            ).first()

            if not user:
                return Response(status=401)

            if not user.check_auth_level(auth_levels):
                return Response(status=403)

            return func(*args, **kwargs)

        return wrapper
    return decorator