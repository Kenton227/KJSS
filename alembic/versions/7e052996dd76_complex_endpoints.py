"""complex endpoints

Revision ID: 7e052996dd76
Revises: 91f8e0f016a5
Create Date: 2025-05-28 03:20:15.608097

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7e052996dd76"
down_revision: Union[str, None] = "91f8e0f016a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users", sa.Column("status", sa.TEXT, nullable=False, server_default="normal")
    )
    op.create_table(
        "showcase_views",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("showcase_id", sa.Integer, sa.ForeignKey("showcases.id", ondelete="CASCADE")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("liked", sa.BOOLEAN, nullable=False, server_default="False"),
        sa.Column(
            "view_timestamp",
            sa.TIMESTAMP,
            nullable=False,
            server_default=sa.sql.func.now(),
        ),
        sa.Column(
            "liked_timestamp",
            sa.TIMESTAMP,
            nullable=True,
            server_default=sa.sql.func.now(),
        ),
        sa.UniqueConstraint("showcase_id", "user_id", name="unique_like"),
    )

    op.drop_table("user_showcase_likes")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "user_showcase_likes",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column(
            "showcase_id", sa.Integer, sa.ForeignKey("showcases.id", ondelete="CASCADE")
        ),
        sa.Column("liked", sa.Boolean, nullable=False, server_default=sa.text("FALSE")),
        sa.Column(
            "disliked", sa.Boolean, nullable=False, server_default=sa.text("FALSE")
        ),
        sa.PrimaryKeyConstraint("user_id", "showcase_id", name="likes_pk"),
        sa.CheckConstraint(
            "liked = FALSE OR disliked = FALSE", name="check_liked_disliked_exclusivity"
        ),
    )

    op.drop_table("showcase_views")
    op.drop_column("users", "status")
