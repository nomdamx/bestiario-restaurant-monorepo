from math import ceil

from sqlalchemy.orm import Session

from src.core.api_response import Pagination
from src.core.custom_errors import ValidationError
from src.core.dependency import BaseFilter, PaginationParams
from src.models import Product, User

from . import schema, service


def get_all(
    db: Session, *, pagination: PaginationParams, filters: BaseFilter
) -> tuple[list[Product], Pagination]:
    categories, total = service.get_paginated(
        db, filters=filters, limit=pagination.limit, offset=pagination.offset
    )
    pages = ceil(total / pagination.limit)

    return categories, Pagination(
        page=pagination.page, pages=pages, limit=pagination.limit, total=total
    )


def get_by_id(db: Session, *, id_product: int) -> Product:
    return service.get_by_id(db, id_product=id_product)


def register(db: Session, *, payload: schema.PayloadProduct) -> Product:
    return service.register(db, payload=payload)


def patch(
    db: Session, *, payload: schema.PayloadUpdateProduct, id_product: int
) -> Product:
    return service.patch(db, payload=payload, id_product=id_product)


def patch_price(
    db: Session, *, payload: schema.PayloadUpdatePriceProduct, id_product: int
) -> Product:
    return service.patch_price(db, payload=payload, id_product=id_product)


def delete(db: Session, *, id_product: int):
    service.soft_delete(db, id_product=id_product)
