from fastapi import APIRouter, status

from src.core.api_response import APIResponse, build_response
from src.core.auth_dependency import StaffDependency, UserDependency
from src.core.dependency import PaginationDependency
from src.db.session import DbSession

from . import controller, dependency, schema

router = APIRouter(prefix="/restaurant-table", tags=["restaurant_table"])

RESPONSE_TYPE = "restaurant_tables"


@router.get("/", response_model=APIResponse[schema.ResponseRestaurantTable])
def route_get_all(
    db: DbSession,
    user: UserDependency,
    pagination: PaginationDependency,
    filters: dependency.FilterRestaurantTableDependency,
):
    restaurant_table, pagination_meta = controller.get_all(
        db, pagination=pagination, filters=filters
    )
    return build_response(
        restaurant_table, response_type=RESPONSE_TYPE, pagination=pagination_meta
    )


@router.post(
    "/",
    response_model=APIResponse[schema.ResponseRestaurantTable],
    status_code=status.HTTP_201_CREATED,
)
def route_register(
    db: DbSession, user: UserDependency, payload: schema.PayloadRestaurantTable
):
    restaurant_table = controller.register(db, payload=payload)
    return build_response(restaurant_table, response_type=RESPONSE_TYPE)


@router.get(
    "/{id_restaurant_table}", response_model=APIResponse[schema.ResponseRestaurantTable]
)
def route_get_by_id(db: DbSession, user: UserDependency, id_restaurant_table: int):
    restaurant_table = controller.get_by_id(db, id_restaurant_table=id_restaurant_table)
    return build_response(restaurant_table, response_type=RESPONSE_TYPE)


@router.patch(
    "/{id_restaurant_table}", response_model=APIResponse[schema.ResponseRestaurantTable]
)
def route_patch(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdateRestaurantTable,
    id_restaurant_table: int,
):
    restaurant_table = controller.patch(
        db, payload=payload, id_restaurant_table=id_restaurant_table
    )
    return build_response(restaurant_table, response_type=RESPONSE_TYPE)


@router.delete("/{id_restaurant_table}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete(db: DbSession, user: StaffDependency, id_restaurant_table: int):
    controller.delete(db, id_restaurant_table=id_restaurant_table)
