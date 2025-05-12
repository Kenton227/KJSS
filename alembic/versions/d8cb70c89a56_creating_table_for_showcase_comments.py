"""creating table for showcase comments

Revision ID: d8cb70c89a56
Revises: ae68eccc1992
Create Date: 2025-05-11 21:19:45.063170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8cb70c89a56'
down_revision: Union[str, None] = 'ae68eccc1992'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
    "showcase_comments",
    sa.Column("post_id", sa.Integer, primary_key= True),
    sa.Column("author_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
    sa.Column("showcase_id", sa.Integer, sa.ForeignKey("showcases.id", ondelete="CASCADE")),
    sa.Column("comment", sa.TEXT, nullable=False),
)



def downgrade() -> None:
    op.drop_table("showcase_comments")