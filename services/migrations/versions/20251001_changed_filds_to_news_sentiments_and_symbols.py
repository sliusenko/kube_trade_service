"""create exchange_fees with UUID FK to exchange_symbols
Revision ID: 20251001_create_exchange_fees
Revises: 20251001_add_price_fields
Create Date: 2025-10-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = "20251001_create_exchange_fees"
down_revision = "20251001_add_price_fields"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "exchange_symbols",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("symbol_id", sa.Text, nullable=False),
        sa.Column("symbol", sa.Text, nullable=False, unique=True),
        sa.Column("exchange_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exchanges.id", ondelete="CASCADE"), nullable=False),
        sa.Column("base_asset", sa.Text, nullable=False),
        sa.Column("quote_asset", sa.Text, nullable=False),
        sa.Column("status", sa.Text),
        sa.Column("type", sa.Text, server_default=sa.text("'spot'")),
        sa.Column("base_precision", sa.Integer),
        sa.Column("quote_precision", sa.Integer),
        sa.Column("step_size", sa.Numeric),
        sa.Column("tick_size", sa.Numeric),
        sa.Column("min_qty", sa.Numeric),
        sa.Column("max_qty", sa.Numeric),
        sa.Column("min_notional", sa.Numeric),
        sa.Column("max_notional", sa.Numeric),
        sa.Column("filters", postgresql.JSONB, server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true"), nullable=False),
        sa.Column("fetched_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("exchange_id", "symbol_id", name="uq_exchange_symbol"),
    )

    op.create_table(
        "exchange_fees",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("exchange_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exchanges.id", ondelete="CASCADE"), nullable=False),
        sa.Column("symbol_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exchange_symbols.id", ondelete="CASCADE")),
        sa.Column("volume_threshold", sa.Numeric, nullable=False),
        sa.Column("maker_fee", sa.Numeric),
        sa.Column("taker_fee", sa.Numeric),
        sa.Column("fetched_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )


def downgrade():
    op.drop_table("exchange_fees")
