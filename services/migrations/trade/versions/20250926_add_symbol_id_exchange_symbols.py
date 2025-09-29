"""add column symbol_id to exchange_symbols with unique constraint

Revision ID: a1b2c3d4e5f6
Revises: None
Create Date: 2025-09-26 12:34:56.789012
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "exchange_symbols",
        sa.Column("symbol_id", sa.Text(), nullable=False, server_default="UNKNOWN")
    )
    op.alter_column("exchange_symbols", "symbol_id", server_default=None)
    op.create_unique_constraint(
        "uq_exchange_symbol",
        "exchange_symbols",
        ["exchange_id", "symbol_id"]
    )


def downgrade():
    op.drop_constraint("uq_exchange_symbol", "exchange_symbols", type_="unique")
    op.drop_column("exchange_symbols", "symbol_id")
