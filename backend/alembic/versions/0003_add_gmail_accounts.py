"""Add Gmail accounts table

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-08 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "gmail_accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("access_token", sa.Text(), nullable=False),
        sa.Column("refresh_token", sa.Text(), nullable=True),
        sa.Column("token_type", sa.String(length=50), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("scope", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_gmail_accounts_id"), "gmail_accounts", ["id"], unique=False)
    op.create_index(op.f("ix_gmail_accounts_user_id"), "gmail_accounts", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_gmail_accounts_user_id"), table_name="gmail_accounts")
    op.drop_index(op.f("ix_gmail_accounts_id"), table_name="gmail_accounts")
    op.drop_table("gmail_accounts")
