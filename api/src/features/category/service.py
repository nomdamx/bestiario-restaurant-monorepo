from sqlalchemy.orm import Query, Session

from src.core.custom_errors import ValidationError
from src.core.dependency import BaseFilter
from src.models import Category

from . import schema


def _query_category_(db: Session) -> Query[Category]:
    return db.query(Category)


def _query_filter_active(db: Session, is_active: bool = True) -> Query[Category]:
    return _query_category_(db).filter(Category.is_active == is_active)


def get_paginated(
    db: Session, *, filters: BaseFilter, limit: int, offset: int
) -> tuple[list[Category], int]:
    categories = _query_filter_active(db, is_active=filters.is_active)
    total = categories.count()

    if total <= 0:
        return categories.all(), 1

    paginated = (
        categories.order_by(Category.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return paginated, total


def get_by_id(db: Session, id_category: int) -> Category:
    category = _query_filter_active(db).filter(Category.id == id_category).first()

    if not category:
        raise ValidationError(details="This Category doesn't exist")

    return category


def register(db: Session, *, payload: schema.PayloadCategory) -> Category:
    register_category = Category(
        name=payload.name,
        ingredient_description=payload.ingredient_description,
        menu_section=payload.menu_section,
    )

    db.add(register_category)
    db.commit()
    return register_category


def patch(
    db: Session, *, payload: schema.PayloadUpdateCategory, id_category: int
) -> Category:
    update_data = payload.model_dump(exclude_unset=True)

    category = _query_filter_active(db).filter(Category.id == id_category).first()

    if not category:
        raise ValidationError(details="This Category doesn't exist")

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    return category


def soft_delete(db: Session, *, id_category: int) -> None:
    category = _query_filter_active(db).filter(Category.id == id_category).first()

    if not category:
        raise ValidationError(details="This Category doesn't exist")

    category.soft_delete()
    db.commit()
