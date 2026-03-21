from math import ceil

from sqlalchemy.orm import Session

from src.core.api_response import Pagination
from src.core.dependency import BaseFilter, PaginationParams
from src.models import ProductAddons, User

from . import schema, service


def get_all(
    db: Session, *, pagination: PaginationParams, filters: BaseFilter
) -> tuple[list[ProductAddons], Pagination]:
    product_addons, total = service.get_paginated(
        db, filters=filters, limit=pagination.limit, offset=pagination.offset
    )
    pages = ceil(total / pagination.limit)

    return product_addons, Pagination(
        page=pagination.page, pages=pages, limit=pagination.limit, total=total
    )


def get_by_id(db: Session, *, id_product_addon: int) -> ProductAddons:
    return service.get_by_id(db, id_product_addon=id_product_addon)


def register(db: Session, *, payload: schema.PayloadProductAddon) -> ProductAddons:
    return service.register(db, payload=payload)


def patch(
    db: Session, *, payload: schema.PayloadUpdateProductAddon, id_product_addon: int
) -> ProductAddons:
    return service.patch(db, payload=payload, id_product_addon=id_product_addon)


def patch_price(
    db: Session,
    *,
    payload: schema.PayloadUpdatePriceProductAddon,
    id_product_addon: int,
) -> ProductAddons:
    return service.patch_price(db, payload=payload, id_product_addon=id_product_addon)


def delete(db: Session, *, id_product_addon: int):
    service.soft_delete(db, id_product_addon=id_product_addon)


def sync_addons_as_products(db: Session):
    service.sync_existing_addons_as_products(db)
