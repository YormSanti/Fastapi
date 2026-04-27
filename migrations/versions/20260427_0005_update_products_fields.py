"""update products fields

Revision ID: 20260427_0005
Revises: 7586a3a25d3a
Create Date: 2026-04-27
"""

from alembic import op
import sqlalchemy as sa


revision = "20260427_0005"
down_revision = "7586a3a25d3a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "products",
        "quantity",
        new_column_name="qty",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.add_column(
        "products",
        sa.Column("category_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "products",
        sa.Column(
            "is_Active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.alter_column(
        "products",
        "is_Active",
        existing_type=sa.Boolean(),
        server_default=None,
        existing_nullable=False,
    )


def downgrade() -> None:
    op.drop_column("products", "updated_at")
    op.drop_column("products", "created_at")
    op.drop_column("products", "is_Active")
    op.drop_column("products", "category_id")
    op.alter_column(
        "products",
        "qty",
        new_column_name="quantity",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
