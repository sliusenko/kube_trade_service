from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "20250929_add_price_history"
down_revision = None   # or the last migration id
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "price_history",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("timestamp", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("exchange", sa.Text, nullable=False),
        sa.Column("pair", sa.Text, nullable=False),
        sa.Column("price", sa.Numeric, nullable=False),
    )
    op.create_index(
        "idx_price_history_pair_time",
        "price_history",
        ["exchange", "pair", "timestamp"]
    )

def downgrade():
    op.drop_index("idx_price_history_pair_time", table_name="price_history")
    op.drop_table("price_history")
