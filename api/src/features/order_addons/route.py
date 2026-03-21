from fastapi import APIRouter, status

from src.core.api_response import APIResponse, build_response
from src.core.auth_dependency import StaffDependency, UserDependency
from src.core.dependency import BaseFilterDependency, PaginationDependency
from src.db.session import DbSession

from . import controller, schema

router = APIRouter(prefix="/order-addon", tags=["order_addon"])

RESPONSE_TYPE = "order_addons"


@router.get("/", response_model=APIResponse[schema.ResponseOrderAddon])
def route_get_all(
    db: DbSession,
    user: UserDependency,
    pagination: PaginationDependency,
    filters: BaseFilterDependency,
):
    order_addons, pagination_meta = controller.get_all(
        db, pagination=pagination, filters=filters
    )
    return build_response(
        order_addons, response_type=RESPONSE_TYPE, pagination=pagination_meta
    )


@router.post(
    "/",
    response_model=APIResponse[schema.ResponseOrderAddon],
    status_code=status.HTTP_201_CREATED,
)
def route_register(
    db: DbSession, user: UserDependency, payload: schema.PayloadOrderAddon
):
    order_addon = controller.register(db, payload=payload)
    return build_response(order_addon, response_type=RESPONSE_TYPE)


@router.get("/{id_order_addon}", response_model=APIResponse[schema.ResponseOrderAddon])
def route_get_by_id(db: DbSession, user: UserDependency, id_order_addon: int):
    order_addon = controller.get_by_id(db, id_order_addon=id_order_addon)
    return build_response(order_addon, response_type=RESPONSE_TYPE)


@router.patch(
    "/{id_order_addon}", response_model=APIResponse[schema.ResponseOrderAddon]
)
def route_patch(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdateOrderAddon,
    id_order_addon: int,
):
    order_addon = controller.patch(db, payload=payload, id_order_addon=id_order_addon)
    return build_response(order_addon, response_type=RESPONSE_TYPE)


@router.delete("/{id_order_addon}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete(db: DbSession, user: StaffDependency, id_order_addon: int):
    controller.delete(db, id_order_addon=id_order_addon)
