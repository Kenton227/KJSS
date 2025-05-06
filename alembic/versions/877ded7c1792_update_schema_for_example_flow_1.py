"""Update schema for Example Flow 1

Revision ID: 877ded7c1792
Revises: e91d0c24f7d0
Create Date: 2025-05-05 12:52:09.487348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '877ded7c1792'
down_revision: Union[str, None] = 'e91d0c24f7d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table("global_inventory")

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("register_date", sa.Integer, primary=True)
    )

    op.create_table(
        "games",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("black", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("white", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("winner", sa.TEXT, nullable=False),
        sa.Column("time_control", sa.TEXT, primary_key=True),
        sa.Column("duration", sa.TIMESTAMP, nullable=False),

        
        sa.CheckConstraint(
            "black != white", 
            name="check_unique_players"
        ),
        sa.CheckConstraint(
            "winner IN ('black', 'white', 'draw')",
            name="check_valid_winner"
        ),
        sa.CheckConstraint(
            "time_control IN ('classical', 'rapid', 'blitz', 'bullet')",
            name="check_valid_time_control"
        )
    )

    op.create_table(
        "showcases",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("title", sa.TEXT, nullable=True, server_default="Untitled"),
        sa.Column("")
    )

    op.create_table(
        "user_showcase_likes",
        sa.Column("user_id", sa.Integer, sa.ForeignKey()),
        sa.Column("showcase_id", sa.Integer, sa.ForeignKey())
    )





def downgrade() -> None:
    """Downgrade schema."""
    pass
