"""Add HubSpot integration fields

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-07 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns to contacts
    op.add_column('contacts', sa.Column('hubspot_id', sa.String(255), nullable=True))
    op.add_column('contacts', sa.Column('source', sa.String(50), nullable=True))
    op.add_column('contacts', sa.Column('last_synced_at', sa.DateTime(), nullable=True))

    # Add columns to companies
    op.add_column('companies', sa.Column('hubspot_id', sa.String(255), nullable=True))
    op.add_column('companies', sa.Column('source', sa.String(50), nullable=True))
    op.add_column('companies', sa.Column('last_synced_at', sa.DateTime(), nullable=True))

    # Add columns to deals
    op.add_column('deals', sa.Column('hubspot_id', sa.String(255), nullable=True))
    op.add_column('deals', sa.Column('source', sa.String(50), nullable=True))
    op.add_column('deals', sa.Column('last_synced_at', sa.DateTime(), nullable=True))

    # Add columns to pipeline_stages
    op.add_column('pipeline_stages', sa.Column('hubspot_id', sa.String(255), nullable=True))
    op.add_column('pipeline_stages', sa.Column('source', sa.String(50), nullable=True))
    op.add_column('pipeline_stages', sa.Column('last_synced_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Remove columns from pipeline_stages
    op.drop_column('pipeline_stages', 'last_synced_at')
    op.drop_column('pipeline_stages', 'source')
    op.drop_column('pipeline_stages', 'hubspot_id')

    # Remove columns from deals
    op.drop_column('deals', 'last_synced_at')
    op.drop_column('deals', 'source')
    op.drop_column('deals', 'hubspot_id')

    # Remove columns from companies
    op.drop_column('companies', 'last_synced_at')
    op.drop_column('companies', 'source')
    op.drop_column('companies', 'hubspot_id')

    # Remove columns from contacts
    op.drop_column('contacts', 'last_synced_at')
    op.drop_column('contacts', 'source')
    op.drop_column('contacts', 'hubspot_id')