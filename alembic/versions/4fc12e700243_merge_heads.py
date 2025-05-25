"""merge heads

Revision ID: 4fc12e700243
Revises: 079499fe7aca, d8cb70c89a56
Create Date: 2025-05-25 14:59:12.518011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fc12e700243'
down_revision: Union[str, None] = ('079499fe7aca', 'd8cb70c89a56')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
