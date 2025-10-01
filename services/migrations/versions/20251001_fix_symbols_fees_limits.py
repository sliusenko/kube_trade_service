from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "20251001_fix_symbols_fees_limits"
down_revision = "93c321294664"
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()

    # ---- exchange_symbols ----
    conn.execute(sa.text("ALTER TABLE exchange_symbols DROP CONSTRAINT IF EXISTS uq_exchange_symbol"))
    op.create_unique_constraint("uq_exchange_symbol", "exchange_symbols", ["exchange_id", "symbol_id"])

    # ---- exchange_fees ----
    conn.execute(sa.text("ALTER TABLE exchange_fees DROP CONSTRAINT IF EXISTS uq_exchange_fees"))
    with op.batch_alter_table("exchange_fees") as batch_op:
        batch_op.alter_column("symbol_id", type_=postgresql.UUID(as_uuid=True))
    op.create_unique_constraint("uq_exchange_fees", "exchange_fees", ["exchange_id", "symbol_id", "volume_threshold"])

    # ---- exchange_limits ----
    conn.execute(sa.text("ALTER TABLE exchange_limits DROP CONSTRAINT IF EXISTS uq_exchange_limits"))
    op.create_unique_constraint("uq_exchange_limits", "exchange_limits", ["exchange_id", "limit_type", "interval_unit", "interval_num"])

def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE exchange_limits DROP CONSTRAINT IF EXISTS uq_exchange_limits"))
    conn.execute(sa.text("ALTER TABLE exchange_fees DROP CONSTRAINT IF EXISTS uq_exchange_fees"))
    conn.execute(sa.text("ALTER TABLE exchange_symbols DROP CONSTRAINT IF EXISTS uq_exchange_symbol"))

    with op.batch_alter_table("exchange_fees") as batch_op:
        batch_op.alter_column("symbol_id", type_=sa.BigInteger)
