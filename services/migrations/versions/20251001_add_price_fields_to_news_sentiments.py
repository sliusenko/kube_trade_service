"""add price fields to news_sentiments

Revision ID: 20251001_add_price_fields
Revises: <тут постав попередній revision>
Create Date: 2025-10-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251001_add_price_fields"
down_revision = "017bc7f249f8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "news_sentiments",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("summary", sa.String(1000)),
        sa.Column("sentiment", sa.Float),
        sa.Column("source", sa.String(80)),
        sa.Column("symbol", sa.String(20), index=True),
        sa.Column("url", sa.String(500)),
        sa.Column("price_before", sa.Numeric(18, 8)),
        sa.Column("price_after_1h", sa.Numeric(18, 8)),
        sa.Column("price_after_6h", sa.Numeric(18, 8)),
        sa.Column("price_after_24h", sa.Numeric(18, 8)),
        sa.Column("price_change_1h", sa.Float),
        sa.Column("price_change_6h", sa.Float),
        sa.Column("price_change_24h", sa.Float),
        sa.UniqueConstraint("published_at", "title", name="uq_news_ts_title"),
    )
