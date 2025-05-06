"""showcases require a game foreign key

Revision ID: ae68eccc1992
Revises: 877ded7c1792
Create Date: 2025-05-06 03:17:14.629039

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ae68eccc1992"
down_revision: Union[str, None] = "877ded7c1792"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "showcases",
        sa.Column("game_id", sa.Integer, sa.ForeignKey("games.id", ondelete="CASCADE")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("showcases", "game_id")
