"""add product category relationship

Revision ID: 20260427_0006
Revises: 20260427_0005
Create Date: 2026-04-27
"""

from alembic import op


revision = "20260427_0006"
down_revision = "20260427_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE products
        SET category_id = NULL
        WHERE category_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM categories
              WHERE categories.id = products.category_id
          )
        """
    )
    op.create_index("ix_products_category_id", "products", ["category_id"])
    op.create_foreign_key(
        "fk_products_category_id_categories",
        "products",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_products_category_id_categories",
        "products",
        type_="foreignkey",
    )
    op.drop_index("ix_products_category_id", table_name="products")
