from math import ceil

from sqlalchemy.orm import Session

from src.core.api_response import Pagination
from src.core.custom_errors import ValidationError
from src.core.dependency import BaseFilter, PaginationParams
from src.models import Category, User

from . import schema, service


def get_all(
    db: Session, *, pagination: PaginationParams, filters: BaseFilter
) -> tuple[list[Category], Pagination]:
    categories, total = service.get_paginated(
        db, filters=filters, limit=pagination.limit, offset=pagination.offset
    )
    pages = ceil(total / pagination.limit)

    return categories, Pagination(
        page=pagination.page, pages=pages, limit=pagination.limit, total=total
    )


def get_by_id(db: Session, *, id_category: int) -> Category:
    return service.get_by_id(db, id_category=id_category)


def register(db: Session, *, payload: schema.PayloadCategory) -> Category:
    return service.register(db, payload=payload)


def patch(
    db: Session, *, payload: schema.PayloadUpdateCategory, id_category: int
) -> Category:
    return service.patch(db, payload=payload, id_category=id_category)


def delete(db: Session, *, id_category: int):
    service.soft_delete(db, id_category=id_category)
