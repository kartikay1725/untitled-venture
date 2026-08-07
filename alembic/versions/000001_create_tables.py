"""Create initial tables for IdeaForge.

Revision ID: 000001
Revises: None
Create Date: 2026-08-07
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "000001"
parent_revisions = (None,)
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "ideas",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("industry_tags", sa.ARRAY(sa.String()), nullable=False, server_default=sa.text("ARRAY[]::text[]")),
        sa.Column("validation_score", sa.Numeric()),
        sa.Column("validation_text", sa.Text()),
        sa.Column("recommended_features", sa.ARRAY(sa.String())),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "mvp_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("idea_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False),
        sa.Column("features", sa.JSONB(), nullable=False),
        sa.Column("generated_code", sa.Text()),
        sa.Column("status", sa.Enum("pending", "ready", "failed", name="mvp_status"), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "deployments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("mvp_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("mvp_templates.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target", sa.String(), nullable=False),
        sa.Column("url", sa.String()),
        sa.Column("status", sa.Enum("queued", "deploying", "success", "error", name="deploy_status"), nullable=False, server_default="queued"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table("deployments")
    op.drop_table("mvp_templates")
    op.drop_table("ideas")
    op.drop_table("users")
