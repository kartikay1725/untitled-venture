"""initial migration

Revision ID: 0001_initial
Revises: 
Create Date: 2026-08-08 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    op.create_table(
        "users",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=sa.text("uuid_generate_v4()")),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    )
    op.create_table(
        "ideas",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("validation_score", sa.Float),
        sa.Column("validated_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    )
    op.create_table(
        "mvp_blueprints",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=sa.text("uuid_generate_v4()")),
        sa.Column("idea_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False),
        sa.Column("wireframes", sa.JSON, nullable=False),
        sa.Column("feature_list", sa.JSON, nullable=False),
        sa.Column("tech_stack", sa.JSON, nullable=False),
        sa.Column("timeline", sa.JSON, nullable=False),
        sa.Column("pdf_url", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    )
    op.create_table(
        "mvp_packages",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=sa.text("uuid_generate_v4()")),
        sa.Column("mvp_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("mvp_blueprints.id", ondelete="CASCADE"), nullable=False),
        sa.Column("zip_url", sa.String(length=255), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    )

def downgrade():
    op.drop_table("mvp_packages")
    op.drop_table("mvp_blueprints")
    op.drop_table("ideas")
    op.drop_table("users")