"""create password reset otps

Revision ID: 20260504_0004
Revises: 20260504_0003
Create Date: 2026-05-04
"""

from alembic import op
import sqlalchemy as sa


revision = "20260504_0004"
down_revision = "20260504_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "password_reset_otps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("otp_hash", sa.String(length=255), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_used", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_password_reset_otps_id"), "password_reset_otps", ["id"], unique=False)
    op.create_index(op.f("ix_password_reset_otps_user_id"), "password_reset_otps", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_password_reset_otps_user_id"), table_name="password_reset_otps")
    op.drop_index(op.f("ix_password_reset_otps_id"), table_name="password_reset_otps")
    op.drop_table("password_reset_otps")
