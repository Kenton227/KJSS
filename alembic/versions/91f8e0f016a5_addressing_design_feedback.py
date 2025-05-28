"""Addressing design feedback

Revision ID: 91f8e0f016a5
Revises: 4fc12e700243
Create Date: 2025-05-27 10:28:24.397420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91f8e0f016a5'
down_revision: Union[str, None] = '4fc12e700243'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "showcase_comments",
        sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.sql.func.now())
    )
    op.add_column(
        "reports",
        sa.Column("status", sa.TEXT, nullable=False, server_default="Pending")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("reports", "status")
    op.drop_column("showcase_comments", "created_at")
