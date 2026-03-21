import secrets
from datetime import UTC, datetime, timedelta
from hashlib import sha256

from src.core.custom_errors import InvalidSession, UserAlreadyExist, ValidationError
from src.db.session import DbSession
from src.models import Session, SystemConfig, User
from src.models.users import AuthLevelUserEnum
from src.utils.dates import create_timestampt, date_now

from .schema import (
    PayloadCreateSession,
    PayloadRegisterUser,
    PayloadToken,
    PayloadValidateUser,
)


def controller_register_user(
    db: DbSession, register_user_request: PayloadRegisterUser
) -> User:
    if user_exist_by_username(db, register_user_request.username):
        raise UserAlreadyExist(details="User must use another username or login")

    registered_user = User(
        username=register_user_request.username,
    )
    registered_user.set_password(register_user_request.password)
    db.add(registered_user)

    db.commit()
    return registered_user


def controller_get_users(db: DbSession) -> list[User]:
    return db.query(User).filter(User.is_active).all()


def controller_delete_user(db: DbSession, id_user: int):
    user = active_users(db).filter_by(id=id_user).first()
    if user is None:
        raise ValidationError(details="User doesn't exist")
    user.soft_delete()
    db.commit()


# AUTH
def controller_validate_user(db: DbSession, user_request: PayloadValidateUser) -> User:
    user = query_username(db, user_request.username)
    if user is None:
        raise ValidationError(details="User doesn't exist or invalid given data")

    need_password = get_need_password(db)
    is_staff = user_is_staff(user)

    if need_password or is_staff:
        if not user.validate_password(user_request.password):
            raise ValidationError(details="Incorrect password")

    return user


def generateSessionToken() -> str:
    return secrets.token_urlsafe(30)


def createSession(db: DbSession, create_session_request: PayloadCreateSession):
    userSessionHash = hash_token(create_session_request.token)

    if not user_exist_by_id(db, create_session_request.id_user):
        raise ValidationError(details="User doesn't exist")

    if session_exist_by_hash(db, userSessionHash):
        raise ValidationError(details="Session already exist")

    registered_session = Session(
        id_user=create_session_request.id_user,
        session=userSessionHash,
        expires_at=create_session_request.expires_at,
    )
    db.add(registered_session)
    db.commit()


def validateSession(db: DbSession, token_request: PayloadToken) -> Session:
    userSessionHash = hash_token(token_request.token)
    session = db.query(Session).filter_by(session=userSessionHash).first()

    if session is None:
        raise InvalidSession()

    expiration_date = datetime.fromtimestamp(timestamp=session.expires_at, tz=UTC)
    now = date_now()
    if now >= expiration_date or not session.user.is_active:
        db.delete(session)
        raise InvalidSession(details="Session has expired")

    if now >= (expiration_date - timedelta(days=15)):
        session.expires_at = create_timestampt()
        db.flush()

    db.commit()
    return session


def invalidateSession(db: DbSession, token_request: PayloadToken):
    userSessionHash = hash_token(token_request.token)
    session = db.query(Session).filter_by(session=userSessionHash).first()
    if session is None:
        raise InvalidSession(details="Session doesn't exist")
    db.delete(session)
    db.commit()


def system_need_password(db: DbSession) -> SystemConfig:
    system = (
        db.query(SystemConfig).filter(SystemConfig.key == "user_need_password").first()
    )
    if system is None:
        raise ValidationError(details="SystemConfig database error")

    return system


def system_admin_config(db: DbSession) -> SystemConfig:
    system = (
        db.query(SystemConfig).filter(SystemConfig.key == "admin_see_config").first()
    )

    if system is None:
        raise ValidationError(details="SystemConfig database error")

    return system


# HELPERS
def user_exist_by_username(db: DbSession, username: str) -> bool:
    return True if query_username(db, username) else False


def user_exist_by_id(db: DbSession, id_user: int) -> bool:
    return True if active_users(db).filter_by(id=id_user).first() else False


def query_username(db: DbSession, username: str) -> User | None:
    return active_users(db).filter_by(username=username).first()


def active_users(db: DbSession):
    return db.query(User).filter_by(is_active=True)


def user_is_staff(user: User) -> bool:
    return user.auth_level.value in [
        AuthLevelUserEnum.ADMIN.value,
        AuthLevelUserEnum.MANAGER.value,
    ]


def session_exist_by_hash(db: DbSession, session: str):
    return True if db.query(Session).filter_by(session=session).first() else False


def hash_token(token: str) -> str:
    return sha256(token.encode("utf-8"), usedforsecurity=True).hexdigest()


def get_need_password(db: DbSession) -> bool:
    return system_need_password(db).value == "true"
