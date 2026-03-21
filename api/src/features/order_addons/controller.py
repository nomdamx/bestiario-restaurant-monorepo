from math import ceil

from sqlalchemy.orm import Session

from src.core.api_response import Pagination
from src.core.custom_errors import ValidationError
from src.core.dependency import BaseFilter, PaginationParams
from src.models import OrderAddons, User

from . import schema, service


def get_all(
    db: Session, *, pagination: PaginationParams, filters: BaseFilter
) -> tuple[list[OrderAddons], Pagination]:
    order_addons, total = service.get_paginated(
        db, filters=filters, limit=pagination.limit, offset=pagination.offset
    )
    pages = ceil(total / pagination.limit)

    return order_addons, Pagination(
        page=pagination.page, pages=pages, limit=pagination.limit, total=total
    )


def get_by_id(db: Session, *, id_order_addon: int) -> OrderAddons:
    return service.get_by_id(db, id_order_addon=id_order_addon)


def register(db: Session, *, payload: schema.PayloadOrderAddon) -> OrderAddons:
    return service.register(db, payload=payload)


def patch(
    db: Session, *, payload: schema.PayloadUpdateOrderAddon, id_order_addon: int
) -> OrderAddons:
    return service.patch(db, payload=payload, id_order_addon=id_order_addon)


def delete(db: Session, *, id_order_addon: int):
    service.soft_delete(db, id_order_addon=id_order_addon)
