import uuid

from fastapi import APIRouter, status

from src.core.api_response import APIResponse, build_response
from src.db.session import DbSession

from . import controller
from .schema import (
    PayloadCreateSession,
    PayloadRegisterUser,
    PayloadSystemValue,
    PayloadToken,
    PayloadValidateUser,
    ResponseSession,
    ResponseToken,
    ResponseUser,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
def route_register_user(db: DbSession, register_user_request: PayloadRegisterUser):
    user = controller.controller_register_user(db, register_user_request)
    return ResponseUser.model_validate(user)


@router.get(
    "/user",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[ResponseUser],
)
def route_get_users(db: DbSession):
    users = controller.controller_get_users(db)
    return build_response(users, response_type="users")


# AUTH
@router.post("/user/validate", response_model=ResponseUser)
def route_validate_user(db: DbSession, user_request: PayloadValidateUser):
    return controller.controller_validate_user(db, user_request)


@router.get("/session/token", response_model=ResponseToken)
def route_session_token():
    return ResponseToken(token=controller.generateSessionToken())


@router.post("/session", status_code=status.HTTP_201_CREATED)
def route_create_session(db: DbSession, create_session_request: PayloadCreateSession):
    controller.createSession(db, create_session_request)


@router.post("/session/validation", response_model=ResponseSession)
def route_validate_session(db: DbSession, token_request: PayloadToken):
    return controller.validateSession(db, token_request)


@router.delete("/session", status_code=status.HTTP_204_NO_CONTENT)
def route_invalidate_session(db: DbSession, token_request: PayloadToken):
    controller.invalidateSession(db, token_request)


@router.get(
    "/system/password",
    status_code=status.HTTP_200_OK,
    response_model=PayloadSystemValue,
)
def route_system_need_password(db: DbSession):
    return controller.system_need_password(db)


@router.get(
    "/system/config",
    status_code=status.HTTP_200_OK,
    response_model=PayloadSystemValue,
)
def route_system_admin_config(db: DbSession):
    return controller.system_admin_config(db)


# ID
@router.delete("/user/{id_user}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete_user(db: DbSession, id_user: int):
    controller.controller_delete_user(db, id_user)
