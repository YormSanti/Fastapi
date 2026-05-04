"""add order detail relationships

Revision ID: 20260504_0001
Revises: 9d7a30cf7587
Create Date: 2026-05-04
"""

from alembic import op


revision = "20260504_0001"
down_revision = "9d7a30cf7587"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE "orderDetails"
        SET order_id = NULL
        WHERE order_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM orders
              WHERE orders.order_id = "orderDetails".order_id
          )
        """
    )
    op.execute(
        """
        UPDATE "orderDetails"
        SET product_id = NULL
        WHERE product_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM products
              WHERE products.id = "orderDetails".product_id
          )
        """
    )
    op.create_index(
        "ix_orderDetails_order_id",
        "orderDetails",
        ["order_id"],
    )
    op.create_index(
        "ix_orderDetails_product_id",
        "orderDetails",
        ["product_id"],
    )
    op.create_foreign_key(
        "fk_orderDetails_order_id_orders",
        "orderDetails",
        "orders",
        ["order_id"],
        ["order_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_orderDetails_product_id_products",
        "orderDetails",
        "products",
        ["product_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_orderDetails_product_id_products",
        "orderDetails",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_orderDetails_order_id_orders",
        "orderDetails",
        type_="foreignkey",
    )
    op.drop_index("ix_orderDetails_product_id", table_name="orderDetails")
    op.drop_index("ix_orderDetails_order_id", table_name="orderDetails")
