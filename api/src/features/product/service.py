from sqlalchemy.orm import Query, Session

from src.core.custom_errors import ValidationError
from src.core.dependency import BaseFilter
from src.models import Order, PriceHistory, Product, Ticket

from . import schema


def _query_product_(db: Session) -> Query[Product]:
    return db.query(Product)


def _query_filter_active(db: Session, is_active: bool = True) -> Query[Product]:
    return _query_product_(db).filter(Product.is_active == is_active)


def get_paginated(
    db: Session, *, filters: BaseFilter, limit: int, offset: int
) -> tuple[list[Product], int]:
    categories = _query_filter_active(db, is_active=filters.is_active)
    total = categories.count()

    if total <= 0:
        return categories.all(), 1

    paginated = (
        categories.order_by(Product.created_at.desc()).limit(limit).offset(offset).all()
    )

    return paginated, total


def get_by_id(db: Session, id_product: int) -> Product:
    product = _query_filter_active(db).filter(Product.id == id_product).first()

    if not product:
        raise ValidationError(details="This Product doesn't exist")

    return product


def register(db: Session, *, payload: schema.PayloadProduct) -> Product:
    register_product = Product(
        name=payload.name,
        complete_name=payload.complete_name if payload.complete_name else payload.name,
        id_category=payload.id_category,
        ingredient_description=payload.ingredient_description,
        price=payload.price,
    )

    db.add(register_product)
    db.commit()
    return register_product


def patch(
    db: Session, *, payload: schema.PayloadUpdateProduct, id_product: int
) -> Product:
    update_data = payload.model_dump(exclude_unset=True)

    product = _query_filter_active(db).filter(Product.id == id_product).first()

    if not product:
        raise ValidationError(details="This Product doesn't exist")

    block_if_active_orders(db, id_product=product.id)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    return product


def patch_price(
    db: Session, *, payload: schema.PayloadUpdatePriceProduct, id_product: int
) -> Product:
    product = _query_filter_active(db).filter(Product.id == id_product).first()

    if not product:
        raise ValidationError(details="This Product doesn't exist")

    block_if_active_orders(db, id_product=product.id)

    if product.id_source_addon:
        raise ValidationError(
            details="Update the Product Addon associated with this Product"
        )

    new_price = payload.price
    old_price = product.price

    if old_price != new_price:
        price_history = PriceHistory(
            product_id=product.id, old_price=old_price, new_price=new_price
        )
        db.add(price_history)

        product.price = new_price
        db.commit()
    return product


def soft_delete(db: Session, *, id_product: int) -> None:
    product = _query_filter_active(db).filter(Product.id == id_product).first()

    if not product:
        raise ValidationError(details="This Product doesn't exist")

    product.soft_delete()
    db.commit()


## EVENTS
def block_if_active_orders(db: Session, *, id_product: int):
    active_order = (
        db.query(Order)
        .join(Ticket, Order.id_ticket == Ticket.id)
        .filter(Order.id_product == id_product)
        .filter(Ticket.is_paid.is_(False))
        .filter(Ticket.is_active)
        .first()
    )

    if active_order:
        raise ValidationError(
            details="Can't be modified while there are active tickets"
        )
