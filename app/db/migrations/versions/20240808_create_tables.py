"""Alembic migration for creating core tables with constraints."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20240808_create_tables"
down_revision = None
branch_labels = None
depends_on = None


# Helper for UUID type
UUID = postgresql.UUID


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "ideas",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("validation_score", sa.Float, nullable=True),
        sa.Column("validated_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "mvp_blueprints",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("idea_id", UUID(as_uuid=True), sa.ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("wireframes", sa.JSON, nullable=False),
        sa.Column("feature_list", sa.JSON, nullable=False),
        sa.Column("tech_stack", sa.JSON, nullable=False),
        sa.Column("timeline", sa.JSON, nullable=False),
        sa.Column("pdf_url", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "mvp_packages",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("mvp_id", UUID(as_uuid=True), sa.ForeignKey("mvp_blueprints.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("zip_url", sa.String(255), nullable=False),
        sa.Column("generated_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )

    # Indexes for performance
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_ideas_user_id", "ideas", ["user_id"])
    op.create_index("ix_mvp_blueprints_idea_id", "mvp_blueprints", ["idea_id"], unique=True)
    op.create_index("ix_mvp_packages_mvp_id", "mvp_packages", ["mvp_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_mvp_packages_mvp_id", table_name="mvp_packages")
    op.drop_index("ix_mvp_blueprints_idea_id", table_name="mvp_blueprints")
    op.drop_index("ix_ideas_user_id", table_name="ideas")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("mvp_packages")
    op.drop_table("mvp_blueprints")
    op.drop_table("ideas")
    op.drop_table("users")
