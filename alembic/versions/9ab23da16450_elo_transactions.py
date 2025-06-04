"""elo transactions

Revision ID: 9ab23da16450
Revises: 7e052996dd76
Create Date: 2025-06-02 12:29:47.642723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ab23da16450'
down_revision: Union[str, None] = '7e052996dd76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "elo_ledger",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("elo_change", sa.Integer),
        sa.Column("game_id", sa.Integer, sa.ForeignKey("games.id"))
    )
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("elo_ledger")
    pass
