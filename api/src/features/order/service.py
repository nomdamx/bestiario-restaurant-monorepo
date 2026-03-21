from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Query, Session

from src.core.custom_errors import ValidationError
from src.core.dependency import BaseFilter
from src.core.recalc_totals import recalc_order_total
from src.features.order_addons.service import get_price_from_addon
from src.models import Order, OrderAddons, Product, ProductAddons

from . import schema


def _query_order_(db: Session) -> Query[Order]:
    return db.query(Order)


def _query_filter_active(db: Session, is_active: bool = True) -> Query[Order]:
    return _query_order_(db).filter(Order.is_active == is_active)


def _make_order(db: Session, *, payload: schema.PayloadOrder) -> Order:
    return Order(
        id_ticket=payload.id_ticket,
        id_product=payload.id_product,
        quantity=payload.quantity,
        finished_status=payload.finished_status,
        unit_price=get_price_from_product(db, id_product=payload.id_product),
    )


def get_paginated(
    db: Session, *, filters: BaseFilter, limit: int, offset: int
) -> tuple[list[Order], int]:
    orders = _query_filter_active(db, is_active=filters.is_active)
    total = orders.count()

    if total <= 0:
        return orders.all(), 1

    paginated = (
        orders.order_by(Order.created_at.desc()).limit(limit).offset(offset).all()
    )

    return paginated, total


def get_by_id(db: Session, id_order: int) -> Order:
    order = _query_filter_active(db).filter(Order.id == id_order).first()

    if not order:
        raise ValidationError(details="This Order doesn't exist")

    return order


def register(db: Session, *, payload: schema.PayloadOrder) -> Order:
    register_order = _make_order(db, payload=payload)

    db.add(register_order)
    db.flush()
    recalc_order_total(db, id_order=register_order.id)
    db.commit()
    return register_order


def register_with_addons(
    db: Session, *, payload: schema.PayloadOrderWithAddons
) -> Order:

    found_ids = (
        db.query(ProductAddons.id)
        .filter(ProductAddons.id.in_(payload.order_addons), ProductAddons.is_active)
        .all()
    )

    found_ids = {row.id for row in found_ids}
    missing = set(payload.order_addons) - found_ids
    if missing:
        raise ValidationError(details=f"Addons not found: {missing}")

    register_order = _make_order(db, payload=payload)

    db.add(register_order)

    if found_ids:
        db.flush()
        db.execute(
            insert(OrderAddons),
            [
                {
                    "id_order": register_order.id,
                    "id_product_addons": addon_id,
                    "unit_price": get_price_from_addon(db, id_product_addon=addon_id),
                }
                for addon_id in found_ids
            ],
        )
    db.flush()
    recalc_order_total(db, id_order=register_order.id)
    db.commit()
    return register_order


def patch(db: Session, *, payload: schema.PayloadUpdateOrder, id_order: int) -> Order:
    update_data = payload.model_dump(exclude_unset=True)

    order = _query_filter_active(db).filter(Order.id == id_order).first()

    if not order:
        raise ValidationError(details="This Order doesn't exist")

    for field, value in update_data.items():
        setattr(order, field, value)

    db.flush()
    recalc_order_total(db, id_order=order.id)
    db.commit()
    return order


def patch_with_addons(
    db: Session, *, payload: schema.PayloadUpdateOrderWithAddons, id_order: int
) -> Order:
    update_data = payload.model_dump(exclude_unset=True)
    addon_ids: list[int] | None = update_data.pop("order_addons", None)

    order = _query_filter_active(db).filter(Order.id == id_order).first()

    if not order:
        raise ValidationError(details="This Order doesn't exist")

    for field, value in update_data.items():
        setattr(order, field, value)

    # TODO: FIX ADDONS APPEND AND NOT CHECK FOR EXISTING
    if addon_ids is not None:
        for addon_id in addon_ids:
            addon_row = OrderAddons(
                id_order=order.id,
                id_product_addons=addon_id,
                unit_price=get_price_from_addon(db, id_product_addon=addon_id),
            )
            order.order_addons.append(addon_row)

    db.flush()
    recalc_order_total(db, id_order=order.id)
    db.commit()
    return order


def soft_delete(db: Session, *, id_order: int) -> None:
    order = db.query(Order).filter(Order.id == id_order).first()

    if not order:
        raise ValidationError(details="This Order doesn't exist")

    order.soft_delete()
    db.flush()
    recalc_order_total(db, id_order=order.id)
    db.commit()


## EVENT
def get_price_from_product(db: Session, *, id_product: int) -> float:
    product = db.query(Product).filter(Product.id == id_product).first()

    if not product:
        raise ValidationError(details="This Product Addon doesn't exist")

    return product.price
