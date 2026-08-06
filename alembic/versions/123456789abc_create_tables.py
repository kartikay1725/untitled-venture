"""create tables

Revision ID: 123456789abc
Revises: 
Create Date: 2026-08-06 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '123456789abc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table(
        'ideas',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('submitted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('validation_score', sa.Numeric, nullable=True),
        sa.Column('validation_feedback', sa.JSON, nullable=True),
        sa.Column('status', sa.Enum('pending', 'validated', 'rejected', name='idea_status'), nullable=False, server_default='pending'),
    )
    op.create_index('ix_ideas_user_id', 'ideas', ['user_id'])
    op.create_index('ix_ideas_status', 'ideas', ['status'])

    op.create_table(
        'mvp_blueprints',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('idea_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('ideas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('features', sa.JSON, nullable=False),
        sa.Column('timeline', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_mvp_blueprints_idea_id', 'mvp_blueprints', ['idea_id'])


def downgrade():
    op.drop_index('ix_mvp_blueprints_idea_id', table_name='mvp_blueprints')
    op.drop_table('mvp_blueprints')
    op.drop_index('ix_ideas_status', table_name='ideas')
    op.drop_index('ix_ideas_user_id', table_name='ideas')
    op.drop_table('ideas')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
