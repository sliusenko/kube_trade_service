from alembic import op


# revision identifiers
revision = "rename_symbol_to_symbol_id"
down_revision = "20251001_news_symbolid"  # вкажи останню ревізію
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("price_history", "symbol",
                    new_column_name="symbol_id")


def downgrade():
    op.alter_column("price_history", "symbol_id",
                    new_column_name="symbol")
