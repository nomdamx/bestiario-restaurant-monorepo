from fastapi import APIRouter, status

from src.core.api_response import APIResponse, build_response
from src.core.auth_dependency import StaffDependency, UserDependency
from src.core.dependency import BaseFilterDependency, PaginationDependency
from src.db.session import DbSession

from . import controller, schema

router = APIRouter(prefix="/category", tags=["category"])

RESPONSE_TYPE = "categories"


@router.get("/", response_model=APIResponse[schema.ResponseCategory])
def route_get_all(
    db: DbSession,
    user: UserDependency,
    pagination: PaginationDependency,
    filters: BaseFilterDependency,
):
    categories, pagination_meta = controller.get_all(
        db, pagination=pagination, filters=filters
    )
    return build_response(
        categories, response_type=RESPONSE_TYPE, pagination=pagination_meta
    )


@router.get("/menu", response_model=APIResponse[schema.ResponseMenuCategory])
def route_get_menu(
    db: DbSession,
    user: UserDependency,
    pagination: PaginationDependency,
    filters: BaseFilterDependency,
):
    categories, pagination_meta = controller.get_all(
        db, pagination=pagination, filters=filters
    )
    return build_response(
        categories, response_type=RESPONSE_TYPE, pagination=pagination_meta
    )


@router.post(
    "/",
    response_model=APIResponse[schema.ResponseCategory],
    status_code=status.HTTP_201_CREATED,
)
def route_register(
    db: DbSession, user: UserDependency, payload: schema.PayloadCategory
):
    category = controller.register(db, payload=payload)
    return build_response(category, response_type=RESPONSE_TYPE)


@router.get("/{id_category}", response_model=APIResponse[schema.ResponseCategory])
def route_get_by_id(db: DbSession, user: UserDependency, id_category: int):
    category = controller.get_by_id(db, id_category=id_category)
    return build_response(category, response_type=RESPONSE_TYPE)


@router.patch("/{id_category}", response_model=APIResponse[schema.ResponseCategory])
def route_patch(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdateCategory,
    id_category: int,
):
    category = controller.patch(db, payload=payload, id_category=id_category)
    return build_response(category, response_type=RESPONSE_TYPE)


@router.delete("/{id_category}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete(db: DbSession, user: StaffDependency, id_category: int):
    controller.delete(db, id_category=id_category)
