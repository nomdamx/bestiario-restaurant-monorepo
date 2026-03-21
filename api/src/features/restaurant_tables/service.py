from sqlalchemy.orm import Query, Session

from src.core.custom_errors import ValidationError
from src.models import RestaurantTable

from . import dependency, schema


def _query_restaurant_table_(db: Session) -> Query[RestaurantTable]:
    return db.query(RestaurantTable)


def _query_filter_active(db: Session, is_active: bool = True) -> Query[RestaurantTable]:
    return _query_restaurant_table_(db).filter(RestaurantTable.is_active == is_active)


def get_paginated(
    db: Session, *, filters: dependency.FilterRestaurantTable, limit: int, offset: int
) -> tuple[list[RestaurantTable], int]:
    restaurant_table = _query_filter_active(db, is_active=filters.is_active)

    if filters.number is not None:
        restaurant_table = restaurant_table.filter(
            RestaurantTable.number == filters.number
        )

    total = restaurant_table.count()

    if total <= 0:
        return restaurant_table.all(), 1

    paginated = (
        restaurant_table.order_by(RestaurantTable.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return paginated, total


def get_by_id(db: Session, id_restaurant_table: int) -> RestaurantTable:
    restaurant_table = (
        _query_filter_active(db)
        .filter(RestaurantTable.id == id_restaurant_table)
        .first()
    )

    if not restaurant_table:
        raise ValidationError(details="This Restaurant Table doesn't exist")

    return restaurant_table


def register(db: Session, *, payload: schema.PayloadRestaurantTable) -> RestaurantTable:
    register_restaurant_table = RestaurantTable(
        number=payload.number,
    )

    db.add(register_restaurant_table)
    db.commit()
    return register_restaurant_table


def patch(
    db: Session,
    *,
    payload: schema.PayloadUpdateRestaurantTable,
    id_restaurant_table: int,
) -> RestaurantTable:

    restaurant_table = (
        _query_filter_active(db)
        .filter(RestaurantTable.id == id_restaurant_table)
        .first()
    )

    if not restaurant_table:
        raise ValidationError(details="This Restaurant Table doesn't exist")

    if payload.number:
        restaurant_table.number = payload.number

    db.commit()
    return restaurant_table


def soft_delete(db: Session, *, id_restaurant_table: int) -> None:
    restaurant_table = (
        _query_filter_active(db)
        .filter(RestaurantTable.id == id_restaurant_table)
        .first()
    )

    if not restaurant_table:
        raise ValidationError(details="This Restaurant Table doesn't exist")

    restaurant_table.soft_delete()
    db.commit()
