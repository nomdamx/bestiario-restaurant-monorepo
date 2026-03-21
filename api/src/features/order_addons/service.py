from sqlalchemy.orm import Query, Session

from src.core.custom_errors import ValidationError
from src.core.dependency import BaseFilter
from src.core.recalc_totals import recalc_order_total
from src.models import OrderAddons, ProductAddons

from . import schema


def _query_order_addon_(db: Session) -> Query[OrderAddons]:
    return db.query(OrderAddons)


def _query_filter_active(db: Session, is_active: bool = True) -> Query[OrderAddons]:
    return _query_order_addon_(db).filter(OrderAddons.is_active == is_active)


def get_paginated(
    db: Session, *, filters: BaseFilter, limit: int, offset: int
) -> tuple[list[OrderAddons], int]:
    order_addons = _query_filter_active(db, is_active=filters.is_active)
    total = order_addons.count()

    if total <= 0:
        return order_addons.all(), 1

    paginated = (
        order_addons.order_by(OrderAddons.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return paginated, total


def get_by_id(db: Session, id_order_addon: int) -> OrderAddons:
    order_addon = (
        _query_filter_active(db).filter(OrderAddons.id == id_order_addon).first()
    )

    if not order_addon:
        raise ValidationError(details="This Order Addons doesn't exist")

    return order_addon


def register(db: Session, *, payload: schema.PayloadOrderAddon) -> OrderAddons:
    register_order_addon = OrderAddons(
        id_product_addons=payload.id_product_addons,
        id_order=payload.id_order,
        unit_price=get_price_from_addon(db, id_product_addon=payload.id_product_addons),
    )

    db.add(register_order_addon)
    recalc_order_total(db, id_order=register_order_addon.id_order)
    db.commit()
    return register_order_addon


def patch(
    db: Session, *, payload: schema.PayloadUpdateOrderAddon, id_order_addon: int
) -> OrderAddons:
    update_data = payload.model_dump(exclude_unset=True)

    order_addon = (
        _query_filter_active(db).filter(OrderAddons.id == id_order_addon).first()
    )

    if not order_addon:
        raise ValidationError(details="This Order Addons doesn't exist")

    for field, value in update_data.items():
        setattr(order_addon, field, value)

    recalc_order_total(db, id_order=order_addon.id_order)
    db.commit()
    return order_addon


def soft_delete(db: Session, *, id_order_addon: int) -> None:
    order_addon = (
        _query_filter_active(db).filter(OrderAddons.id == id_order_addon).first()
    )

    if not order_addon:
        raise ValidationError(details="This Order Addons doesn't exist")

    order_addon.soft_delete()
    recalc_order_total(db, id_order=order_addon.id)
    db.commit()


## EVENT
def get_price_from_addon(db: Session, *, id_product_addon: int) -> float:
    addon = db.query(ProductAddons).filter(ProductAddons.id == id_product_addon).first()

    if not addon:
        raise ValidationError(details="This Product Addon doesn't exist")

    return addon.price
