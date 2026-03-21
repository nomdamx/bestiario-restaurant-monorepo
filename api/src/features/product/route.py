from fastapi import APIRouter, status

from src.core.api_response import APIResponse, build_response
from src.core.auth_dependency import StaffDependency, UserDependency
from src.core.dependency import BaseFilterDependency, PaginationDependency
from src.db.session import DbSession

from . import controller, schema

router = APIRouter(prefix="/product", tags=["product"])

RESPONSE_TYPE = "products"


@router.get("/", response_model=APIResponse[schema.ResponseProduct])
def route_get_all(
    db: DbSession,
    user: UserDependency,
    pagination: PaginationDependency,
    filters: BaseFilterDependency,
):
    products, pagination_meta = controller.get_all(
        db, pagination=pagination, filters=filters
    )
    return build_response(
        products, response_type=RESPONSE_TYPE, pagination=pagination_meta
    )


@router.post(
    "/",
    response_model=APIResponse[schema.ResponseProduct],
    status_code=status.HTTP_201_CREATED,
)
def route_register(db: DbSession, user: UserDependency, payload: schema.PayloadProduct):
    product = controller.register(db, payload=payload)
    return build_response(product, response_type=RESPONSE_TYPE)


@router.get("/{id_product}", response_model=APIResponse[schema.ResponseProduct])
def route_get_by_id(db: DbSession, user: UserDependency, id_product: int):
    product = controller.get_by_id(db, id_product=id_product)
    return build_response(product, response_type=RESPONSE_TYPE)


@router.patch("/{id_product}", response_model=APIResponse[schema.ResponseProduct])
def route_patch(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdateProduct,
    id_product: int,
):
    product = controller.patch(db, payload=payload, id_product=id_product)
    return build_response(product, response_type=RESPONSE_TYPE)


@router.patch("/{id_product}/price", response_model=APIResponse[schema.ResponseProduct])
def route_patch_price(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdatePriceProduct,
    id_product: int,
):
    product = controller.patch_price(db, payload=payload, id_product=id_product)
    return build_response(product, response_type=RESPONSE_TYPE)


@router.delete("/{id_product}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete(db: DbSession, user: StaffDependency, id_product: int):
    controller.delete(db, id_product=id_product)
