"""Add complete_name to Product

Revision ID: f547e6aa09b6
Revises: ec793d211468
Create Date: 2026-01-07 16:25:48.534106
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f547e6aa09b6'
down_revision = 'ec793d211468'
branch_labels = None
depends_on = None


def upgrade():
    # 1️⃣ Agregar columna como nullable
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('complete_name', sa.String(), nullable=True)
        )

    # 2️⃣ Copiar name → complete_name en registros existentes
    op.execute("""
        UPDATE product
        SET complete_name = name
        WHERE complete_name IS NULL
    """)

    # 3️⃣ Cambiar a NOT NULL
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column(
            'complete_name',
            nullable=False
        )


def downgrade():
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('complete_name')
