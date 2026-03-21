from fastapi import APIRouter, status

from src.core.api_response import APIResponse, build_response
from src.core.auth_dependency import StaffDependency, UserDependency
from src.core.dependency import BaseFilterDependency, PaginationDependency
from src.db.session import DbSession

from . import controller, schema

router = APIRouter(prefix="/order", tags=["order"])

RESPONSE_TYPE = "orders"


@router.get("/", response_model=APIResponse[schema.ResponseOrder])
def route_get_all(
    db: DbSession,
    user: UserDependency,
    pagination: PaginationDependency,
    filters: BaseFilterDependency,
):
    orders, pagination_meta = controller.get_all(
        db, pagination=pagination, filters=filters
    )
    return build_response(
        orders, response_type=RESPONSE_TYPE, pagination=pagination_meta
    )


# @router.post(
#     "/",
#     response_model=APIResponse[schema.ResponseOrder],
#     status_code=status.HTTP_201_CREATED,
# )
# def route_register(db: DbSession, user: UserDependency, payload: schema.PayloadOrder):
#     order = controller.register(db, payload=payload)
#     return build_response(order, response_type=RESPONSE_TYPE)


@router.post(
    "/",
    response_model=APIResponse[schema.ResponseOrder],
    status_code=status.HTTP_201_CREATED,
)
def route_register_with_addons(
    db: DbSession, user: UserDependency, payload: schema.PayloadOrderWithAddons
):
    order = controller.register_with_addon(db, payload=payload)
    return build_response(order, response_type=RESPONSE_TYPE)


@router.get("/{id_order}", response_model=APIResponse[schema.ResponseOrder])
def route_get_by_id(db: DbSession, user: UserDependency, id_order: int):
    order = controller.get_by_id(db, id_order=id_order)
    return build_response(order, response_type=RESPONSE_TYPE)


# @router.patch("/{id_order}", response_model=APIResponse[schema.ResponseOrder])
# def route_patch(
#     db: DbSession,
#     user: UserDependency,
#     payload: schema.PayloadUpdateOrder,
#     id_order: int,
# ):
#     order = controller.patch(db, payload=payload, id_order=id_order)
#     return build_response(order, response_type=RESPONSE_TYPE)


@router.patch("/{id_order}", response_model=APIResponse[schema.ResponseOrder])
def route_patch_with_addons(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdateOrderWithAddons,
    id_order: int,
):
    order = controller.patch_with_addons(db, payload=payload, id_order=id_order)
    return build_response(order, response_type=RESPONSE_TYPE)


@router.delete("/{id_order}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete(db: DbSession, user: UserDependency, id_order: int):
    controller.delete(db, id_order=id_order)
