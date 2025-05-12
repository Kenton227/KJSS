"""Update schema for Example Flow 1

Revision ID: 877ded7c1792
Revises: e91d0c24f7d0
Create Date: 2025-05-05 12:52:09.487348

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "877ded7c1792"
down_revision: Union[str, None] = "e91d0c24f7d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table("global_inventory")

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.TEXT, unique=True),
        sa.Column("email", sa.TEXT, unique=True),
        sa.Column(
            "register_date",
            sa.TIMESTAMP,
            nullable=False,
            server_default=sa.sql.func.now(),
        ),
    )

    op.create_table(
        "games",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("black", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("white", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("winner", sa.TEXT, nullable=False),
        sa.Column("time_control", sa.TEXT, nullable=False),
        sa.Column("duration_in_ms", sa.Integer, nullable=False),
        sa.Column(
            "date_played",
            sa.TIMESTAMP,
            nullable=False,
            server_default=sa.sql.func.now(),
        ),
        sa.CheckConstraint("black != white", name="check_unique_players"),
        sa.CheckConstraint(
            "winner IN ('black', 'white', 'draw')", name="check_valid_winner"
        ),
        sa.CheckConstraint(
            "time_control IN ('classical', 'rapid', 'blitz', 'bullet')",
            name="check_valid_time_control",
        ),
    )

    op.create_table(
        "showcases",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "created_by", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")
        ),
        sa.Column("title", sa.TEXT, nullable=True, server_default="Untitled"),
        sa.Column("views", sa.Integer, nullable=False, server_default="0"),
        sa.Column("caption", sa.TEXT),
        sa.Column(
            "date_created",
            sa.DATE,
            nullable=False,
            server_default=sa.sql.func.current_date(),
        ),
    )

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


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_showcase_likes")
    op.drop_table("showcases")
    op.drop_table("games")
    op.drop_table("users")

    op.create_table(
        "global_inventory",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("gold", sa.Integer, nullable=False),
        sa.CheckConstraint("gold >= 0", name="check_gold_positive"),
    )

    op.execute(sa.text("INSERT INTO global_inventory (gold) VALUES (100)"))
