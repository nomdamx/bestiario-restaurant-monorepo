from math import ceil

from sqlalchemy.orm import Session

from src.core.api_response import Pagination
from src.core.custom_errors import ValidationError
from src.core.dependency import PaginationParams
from src.models import RestaurantTable, User

from . import dependency, schema, service


def get_all(
    db: Session,
    *,
    pagination: PaginationParams,
    filters: dependency.FilterRestaurantTable,
) -> tuple[list[RestaurantTable], Pagination]:
    restaurant_table, total = service.get_paginated(
        db, filters=filters, limit=pagination.limit, offset=pagination.offset
    )
    pages = ceil(total / pagination.limit)

    return restaurant_table, Pagination(
        page=pagination.page, pages=pages, limit=pagination.limit, total=total
    )


def get_by_id(db: Session, *, id_restaurant_table: int) -> RestaurantTable:
    return service.get_by_id(db, id_restaurant_table=id_restaurant_table)


def register(db: Session, *, payload: schema.PayloadRestaurantTable) -> RestaurantTable:
    return service.register(db, payload=payload)


def patch(
    db: Session,
    *,
    payload: schema.PayloadUpdateRestaurantTable,
    id_restaurant_table: int,
) -> RestaurantTable:
    return service.patch(db, payload=payload, id_restaurant_table=id_restaurant_table)


def delete(db: Session, *, id_restaurant_table: int):
    service.soft_delete(db, id_restaurant_table=id_restaurant_table)
