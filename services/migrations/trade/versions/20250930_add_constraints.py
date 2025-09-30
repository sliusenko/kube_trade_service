"""add unique constraints for exchange_limits and exchange_fees

Revision ID: 20250930_add_constraints
Revises: <попередній revision id>
Create Date: 2025-09-30 10:00:00.000000
"""

from alembic import op


# revision identifiers, used by Alembic
revision = "20250930_add_constraints"
down_revision = "<попередній revision id>"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ---- exchange_limits ----
    op.create_unique_constraint(
        "uq_exchange_limits",
        "exchange_limits",
        ["exchange_id", "limit_type", "interval_unit", "interval_num"],
    )

    # ---- exchange_fees ----
    op.create_unique_constraint(
        "uq_exchange_fees",
        "exchange_fees",
        ["exchange_id", "symbol_id", "volume_threshold"],
    )


def downgrade() -> None:
    # ---- exchange_limits ----
    op.drop_constraint("uq_exchange_limits", "exchange_limits", type_="unique")

    # ---- exchange_fees ----
    op.drop_constraint("uq_exchange_fees", "exchange_fees", type_="unique")
