from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Query, Session

from src.core.custom_errors import ValidationError
from src.core.dependency import BaseFilter
from src.models import (
    Category,
    Order,
    OrderAddons,
    PriceHistory,
    Product,
    ProductAddons,
    Ticket,
)

from . import schema


def _query_product_addon_(db: Session) -> Query[ProductAddons]:
    return db.query(ProductAddons)


def _query_filter_active(db: Session, is_active: bool = True) -> Query[ProductAddons]:
    return _query_product_addon_(db).filter(ProductAddons.is_active == is_active)


def get_paginated(
    db: Session, *, filters: BaseFilter, limit: int, offset: int
) -> tuple[list[ProductAddons], int]:
    product_addon = _query_filter_active(db, is_active=filters.is_active)
    total = product_addon.count()

    if total <= 0:
        return product_addon.all(), 1

    paginated = (
        product_addon.order_by(ProductAddons.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return paginated, total


def get_by_id(db: Session, id_product_addon: int) -> ProductAddons:
    product_addon = (
        _query_filter_active(db).filter(ProductAddons.id == id_product_addon).first()
    )

    if not product_addon:
        raise ValidationError(details="This Product Addon doesn't exist")

    return product_addon


def register(db: Session, *, payload: schema.PayloadProductAddon) -> ProductAddons:
    register_product_addon = ProductAddons(
        name=payload.name, type=payload.type, price=payload.price
    )

    db.add(register_product_addon)
    db.flush()

    extras_category = get_or_create_extras_category(db)

    product = Product(
        name=register_product_addon.name,
        complete_name=register_product_addon.name,
        price=register_product_addon.price,
        id_category=extras_category.id,
        id_source_addon=register_product_addon.id,
    )
    db.add(product)

    db.commit()
    return register_product_addon


def patch(
    db: Session, *, payload: schema.PayloadUpdateProductAddon, id_product_addon: int
) -> ProductAddons:
    update_data = payload.model_dump(exclude_unset=True)

    product_addon = (
        _query_filter_active(db).filter(ProductAddons.id == id_product_addon).first()
    )

    if not product_addon:
        raise ValidationError(details="This Product Addon doesn't exist")

    for field, value in update_data.items():
        setattr(product_addon, field, value)

    db.commit()
    return product_addon


def patch_price(
    db: Session,
    *,
    payload: schema.PayloadUpdatePriceProductAddon,
    id_product_addon: int,
) -> ProductAddons:
    product_addon = (
        _query_filter_active(db).filter(ProductAddons.id == id_product_addon).first()
    )

    if not product_addon:
        raise ValidationError(details="This Product Addon doesn't exist")

    block_if_active_orders(db, id_product_addon=product_addon.id)

    product = (
        db.query(Product).filter(Product.id_source_addon == product_addon.id).first()
    )

    if not product:
        raise ValidationError(
            details="There is not Product attached to this Addon, sync first"
        )

    new_price = payload.price
    old_price = product_addon.price

    if old_price != new_price:
        price_history = PriceHistory(
            product_id=product.id, old_price=old_price, new_price=new_price
        )

        db.add(price_history)

        product_addon.price = new_price
        product.price = new_price
        db.commit()

    return product_addon


def soft_delete(db: Session, *, id_product_addon: int) -> None:
    product_addon = (
        _query_filter_active(db).filter(ProductAddons.id == id_product_addon).first()
    )

    if not product_addon:
        raise ValidationError(details="This Product Addon doesn't exist")

    product = (
        db.query(Product).filter(Product.id_source_addon == product_addon.id).first()
    )

    if not product:
        raise ValidationError(details="There is not Product attached to this Addon")

    product_addon.soft_delete()
    product.soft_delete()
    db.commit()


def sync_existing_addons_as_products(db: Session):
    extra_category = get_or_create_extras_category(db)
    addons = (
        db.query(ProductAddons)
        .outerjoin(Product, Product.id_source_addon == ProductAddons.id)
        .all()
    )
    if not addons:
        return

    db.execute(
        insert(Product),
        [
            {
                "name": addon.name,
                "complete_name": addon.name,
                "price": addon.price,
                "id_category": extra_category.id,
                "id_source_addon": addon.id,
            }
            for addon in addons
        ],
    )
    db.commit()


## EVENTS
def get_or_create_extras_category(db: Session):
    category = db.query(Category).filter(Category.name == "Extras").first()
    if not category:
        category = Category(
            name="Extras", ingredient_description="Extras para agregar por separado."
        )
        db.add(category)
        db.commit()
    return category


def block_if_active_orders(db: Session, *, id_product_addon: int):
    active_order = (
        db.query(OrderAddons)
        .join(Order, OrderAddons.id_order == Order.id)
        .join(Ticket, Ticket.id == Order.id_ticket)
        .filter(OrderAddons.id_product_addons == id_product_addon)
        .filter(Ticket.is_paid.is_(False))
        .filter(Ticket.is_active)
        .first()
    )

    if active_order:
        raise ValidationError(
            details="Can't be modified while there are active tickets"
        )
