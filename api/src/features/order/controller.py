from math import ceil

from sqlalchemy.orm import Session

from src.core.api_response import Pagination
from src.core.custom_errors import ValidationError
from src.core.dependency import BaseFilter, PaginationParams
from src.models import Order, User

from . import schema, service


def get_all(
    db: Session, *, pagination: PaginationParams, filters: BaseFilter
) -> tuple[list[Order], Pagination]:
    orders, total = service.get_paginated(
        db, filters=filters, limit=pagination.limit, offset=pagination.offset
    )
    pages = ceil(total / pagination.limit)

    return orders, Pagination(
        page=pagination.page, pages=pages, limit=pagination.limit, total=total
    )


def get_by_id(db: Session, *, id_order: int) -> Order:
    return service.get_by_id(db, id_order=id_order)


def register(db: Session, *, payload: schema.PayloadOrder) -> Order:
    return service.register(db, payload=payload)


def register_with_addon(
    db: Session, *, payload: schema.PayloadOrderWithAddons
) -> Order:
    return service.register_with_addons(db, payload=payload)


def patch(db: Session, *, payload: schema.PayloadUpdateOrder, id_order: int) -> Order:
    return service.patch(db, payload=payload, id_order=id_order)


def patch_with_addons(
    db: Session, *, payload: schema.PayloadUpdateOrderWithAddons, id_order: int
) -> Order:
    return service.patch_with_addons(db, payload=payload, id_order=id_order)


def delete(db: Session, *, id_order: int):
    service.soft_delete(db, id_order=id_order)
