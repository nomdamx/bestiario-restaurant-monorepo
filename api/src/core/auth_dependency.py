from hashlib import sha256
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.custom_errors import AuthError
from src.db.session import DbSession
from src.models.users import AuthLevelUserEnum, Session, User

security = HTTPBearer()

security_dependency = Annotated[HTTPAuthorizationCredentials, Depends(security)]


def hash_token(token: str) -> str:
    return sha256(token.encode("utf-8"), usedforsecurity=True).hexdigest()


def get_user_by_token(
    db: DbSession,
    credentials: security_dependency,
) -> User:
    token = credentials.credentials
    if not token:
        raise AuthError(details="Missing token session")

    userSessionHash = hash_token(token)
    session = db.query(Session).filter_by(session=userSessionHash).first()
    if session is None:
        raise AuthError(details="Invalid token session")
    return session.user


UserDependency = Annotated[User, Depends(get_user_by_token)]


def require_auth(auth_roles: list[AuthLevelUserEnum]):
    def dependency(user: UserDependency):
        if not user.check_auth(auth_roles):
            raise AuthError(details="Not authorized")
        return user

    return dependency


AdminDependency = Annotated[User, Depends(require_auth([AuthLevelUserEnum.ADMIN]))]

StaffDependency = Annotated[
    User, Depends(require_auth([AuthLevelUserEnum.ADMIN, AuthLevelUserEnum.MANAGER]))
]
