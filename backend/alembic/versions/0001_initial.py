"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-05-06 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=150), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=256), nullable=False),
        sa.Column('full_name', sa.String(length=150), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='user'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('industry', sa.String(length=120), nullable=True),
        sa.Column('website', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=120), nullable=False),
        sa.Column('last_name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('company_id', sa.Integer(), sa.ForeignKey('companies.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'deals',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=220), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('stage', sa.String(length=120), nullable=False, server_default='Lead'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='Open'),
        sa.Column('contact_id', sa.Integer(), sa.ForeignKey('contacts.id'), nullable=True),
        sa.Column('company_id', sa.Integer(), sa.ForeignKey('companies.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'pipeline_stages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('step_order', sa.Integer(), nullable=False),
    )
    op.create_table(
        'email_templates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=150), nullable=False, unique=True),
        sa.Column('subject', sa.String(length=220), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_table(
        'activities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_type', sa.String(length=120), nullable=False),
        sa.Column('payload', sa.Text(), nullable=True),
        sa.Column('contact_id', sa.Integer(), sa.ForeignKey('contacts.id'), nullable=True),
        sa.Column('deal_id', sa.Integer(), sa.ForeignKey('deals.id'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )


def downgrade() -> None:
    op.drop_table('activities')
    op.drop_table('email_templates')
    op.drop_table('pipeline_stages')
    op.drop_table('deals')
    op.drop_table('contacts')
    op.drop_table('companies')
    op.drop_table('users')
