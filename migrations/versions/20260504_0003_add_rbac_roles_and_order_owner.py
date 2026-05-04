"""add rbac roles and order owner

Revision ID: 20260504_0003
Revises: 20260504_0002
Create Date: 2026-05-04
"""

from alembic import op
import sqlalchemy as sa


revision = "20260504_0003"
down_revision = "20260504_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.String(length=20), server_default="user", nullable=False),
    )
    op.add_column("orders", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_index("ix_orders_user_id", "orders", ["user_id"])
    op.create_foreign_key(
        "fk_orders_user_id_users",
        "orders",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.execute(
        """
        UPDATE users
        SET role = 'admin'
        WHERE id = (
            SELECT id
            FROM users
            ORDER BY id
            LIMIT 1
        )
        AND NOT EXISTS (
            SELECT 1
            FROM users
            WHERE role = 'admin'
        )
        """
    )


def downgrade() -> None:
    op.drop_constraint("fk_orders_user_id_users", "orders", type_="foreignkey")
    op.drop_index("ix_orders_user_id", table_name="orders")
    op.drop_column("orders", "user_id")
    op.drop_column("users", "role")
