"""Snapshots of prices

Revision ID: ec793d211468
Revises: f94390b8e1aa
Create Date: 2026-01-07 04:22:39.222626
"""

from alembic import op
import sqlalchemy as sa


revision = 'ec793d211468'
down_revision = 'f94390b8e1aa'
branch_labels = None
depends_on = None


def upgrade():
    # 1️⃣ Crear columnas como NULLABLE
    with op.batch_alter_table('order') as batch_op:
        batch_op.add_column(sa.Column('unit_price', sa.Float(), nullable=True))

    with op.batch_alter_table('order_addons') as batch_op:
        batch_op.add_column(sa.Column('unit_price', sa.Float(), nullable=True))

    # 2️⃣ Backfill orders.unit_price desde product.price
    op.execute("""
        UPDATE "order" o
        SET unit_price = p.price
        FROM product p
        WHERE o.id_product = p.id
    """)

    # 3️⃣ Backfill order_addons.unit_price desde product_addons.price
    op.execute("""
        UPDATE order_addons oa
        SET unit_price = pa.price
        FROM product_addons pa
        WHERE oa.id_product_addons = pa.id
    """)

    # 4️⃣ Ahora sí: hacer NOT NULL
    with op.batch_alter_table('order') as batch_op:
        batch_op.alter_column('unit_price', nullable=False)

    with op.batch_alter_table('order_addons') as batch_op:
        batch_op.alter_column('unit_price', nullable=False)


def downgrade():
    with op.batch_alter_table('order_addons') as batch_op:
        batch_op.drop_column('unit_price')

    with op.batch_alter_table('order') as batch_op:
        batch_op.drop_column('unit_price')
