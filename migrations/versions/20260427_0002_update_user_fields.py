"""update user fields

Revision ID: 20260427_0002
Revises: 20260427_0001
Create Date: 2026-04-27
"""

from alembic import op
import sqlalchemy as sa


revision = "20260427_0002"
down_revision = "20260427_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("firstName", sa.String(length=100), nullable=True))
    op.add_column("users", sa.Column("lastName", sa.String(length=100), nullable=True))
    op.add_column("users", sa.Column("password", sa.String(length=255), nullable=True))

    op.execute('UPDATE users SET "firstName" = COALESCE(name, \'\')')
    op.execute('UPDATE users SET "lastName" = \'\' WHERE "lastName" IS NULL')
    op.execute('UPDATE users SET "password" = \'\' WHERE "password" IS NULL')

    op.alter_column("users", "firstName", nullable=False)
    op.alter_column("users", "lastName", nullable=False)
    op.alter_column("users", "password", nullable=False)
    op.drop_column("users", "name")


def downgrade() -> None:
    op.add_column("users", sa.Column("name", sa.String(length=100), nullable=True))
    op.execute('UPDATE users SET name = COALESCE("firstName", \'\')')
    op.alter_column("users", "name", nullable=False)

    op.drop_column("users", "password")
    op.drop_column("users", "lastName")
    op.drop_column("users", "firstName")
