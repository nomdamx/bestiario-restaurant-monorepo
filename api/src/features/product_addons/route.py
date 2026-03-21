from fastapi import APIRouter, status

from src.core.api_response import APIResponse, build_response
from src.core.auth_dependency import StaffDependency, UserDependency
from src.core.dependency import BaseFilterDependency, PaginationDependency
from src.db.session import DbSession

from . import controller, schema

router = APIRouter(prefix="/product-addon", tags=["product_addons"])

RESPONSE_TYPE = "product_addons"


@router.get("/", response_model=APIResponse[schema.ResponseProductAddon])
def route_get_all(
    db: DbSession,
    user: UserDependency,
    pagination: PaginationDependency,
    filters: BaseFilterDependency,
):
    product_addons, pagination_meta = controller.get_all(
        db, pagination=pagination, filters=filters
    )
    return build_response(
        product_addons, response_type=RESPONSE_TYPE, pagination=pagination_meta
    )


@router.post(
    "/",
    response_model=APIResponse[schema.ResponseProductAddon],
    status_code=status.HTTP_201_CREATED,
)
def route_register(
    db: DbSession, user: UserDependency, payload: schema.PayloadProductAddon
):
    product_addon = controller.register(db, payload=payload)
    return build_response(product_addon, response_type=RESPONSE_TYPE)


@router.get(
    "/{id_product_addon}", response_model=APIResponse[schema.ResponseProductAddon]
)
def route_get_by_id(db: DbSession, user: UserDependency, id_product_addon: int):
    product_addon = controller.get_by_id(db, id_product_addon=id_product_addon)
    return build_response(product_addon, response_type=RESPONSE_TYPE)


@router.post("/sync", status_code=status.HTTP_201_CREATED)
def route_sync_addons_as_products(db: DbSession, user: StaffDependency):
    controller.sync_addons_as_products(db)


@router.patch(
    "/{id_product_addon}", response_model=APIResponse[schema.ResponseProductAddon]
)
def route_patch(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdateProductAddon,
    id_product_addon: int,
):
    product_addon = controller.patch(
        db, payload=payload, id_product_addon=id_product_addon
    )
    return build_response(product_addon, response_type=RESPONSE_TYPE)


@router.patch(
    "/{id_product_addon}/price", response_model=APIResponse[schema.ResponseProductAddon]
)
def route_patch_price(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdatePriceProductAddon,
    id_product_addon: int,
):
    product_addon = controller.patch_price(
        db, payload=payload, id_product_addon=id_product_addon
    )
    return build_response(product_addon, response_type=RESPONSE_TYPE)


@router.delete("/{id_product_addon}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete(db: DbSession, user: StaffDependency, id_product_addon: int):
    controller.delete(db, id_product_addon=id_product_addon)
