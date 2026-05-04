"""add product name to order details

Revision ID: 20260504_0002
Revises: 20260504_0001
Create Date: 2026-05-04
"""

from alembic import op
import sqlalchemy as sa


revision = "20260504_0002"
down_revision = "20260504_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "orderDetails",
        sa.Column("product_name", sa.String(length=100), nullable=True),
    )
    op.execute(
        """
        UPDATE "orderDetails"
        SET product_name = products."productName"
        FROM products
        WHERE "orderDetails".product_id = products.id
        """
    )
    op.execute(
        """
        UPDATE "orderDetails"
        SET product_name = ''
        WHERE product_name IS NULL
        """
    )
    op.alter_column(
        "orderDetails",
        "product_name",
        existing_type=sa.String(length=100),
        nullable=False,
        server_default="",
    )


def downgrade() -> None:
    op.drop_column("orderDetails", "product_name")
