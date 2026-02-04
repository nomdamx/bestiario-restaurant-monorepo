def recalc_ticket_total(connection, ticket_id):
    from app.models import Ticket, Order
    order_table = Order.__table__
    ticket_table = Ticket.__table__

    totals = connection.execute(
        order_table.select()
        .with_only_columns(order_table.c.total)
        .where(order_table.c.id_ticket == ticket_id)
        .where(order_table.c.is_active == True)
    ).fetchall()

    new_total = float(sum(row.total or 0 for row in totals))

    connection.execute(
        ticket_table.update()
        .where(ticket_table.c.id == ticket_id)
        .values(total=new_total)
    )

def recalc_order_total(connection, order_id):
    from app.models import Product, ProductAddons, OrderAddons, Order
    product_table = Product.__table__
    order_table = Order.__table__
    order_addons_table = OrderAddons.__table__
    product_addons_table = ProductAddons.__table__

    target:Order = connection.execute(
        order_table.select()
        .where(order_table.c.id == order_id)
    ).fetchone()

    product:Product = connection.execute(
        product_table.select()
        .where(product_table.c.id == target.id_product)
        .where(product_table.c.is_active == True)
    ).fetchone()

    order_addons = connection.execute(
        order_addons_table.select()
        .where(order_addons_table.c.id_order == target.id)
        .where(order_addons_table.c.is_active == True)
    ).fetchall()

    new_order_total = 0

    new_order_total = float(target.unit_price * target.quantity)

    if order_addons:
        for addon in order_addons:
            new_order_total += float(addon.unit_price * target.quantity)

    connection.execute(
        order_table.update()
        .where(order_table.c.id == target.id)
        .values(total=new_order_total)
    )

    recalc_ticket_total(
        connection = connection,
        ticket_id = target.id_ticket
    )