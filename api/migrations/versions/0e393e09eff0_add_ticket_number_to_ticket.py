"""Add ticket_number and operational_date to Ticket

Revision ID: 0e393e09eff0
Revises: f547e6aa09b6
Create Date: 2026-01-08 05:43:04.981140
"""

from alembic import op
import sqlalchemy as sa

revision = '0e393e09eff0'
down_revision = 'f547e6aa09b6'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('ticket') as batch_op:
        batch_op.add_column(
            sa.Column('ticket_number', sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('operational_date', sa.Date(), nullable=True)
        )

    op.execute("""
        UPDATE ticket
        SET
            ticket_number = id,
            operational_date = DATE '2026-01-05'
        WHERE ticket_number IS NULL
    """)

    with op.batch_alter_table('ticket') as batch_op:
        batch_op.alter_column(
            'ticket_number',
            nullable=False
        )
        batch_op.alter_column(
            'operational_date',
            nullable=False
        )
        batch_op.create_unique_constraint(
            'uq_ticket_operational_day_number',
            ['operational_date', 'ticket_number']
        )


def downgrade():
    with op.batch_alter_table('ticket') as batch_op:
        batch_op.drop_constraint(
            'uq_ticket_operational_day_number',
            type_='unique'
        )
        batch_op.drop_column('operational_date')
        batch_op.drop_column('ticket_number')
