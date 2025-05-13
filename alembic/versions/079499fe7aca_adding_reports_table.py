"""adding reports table

Revision ID: 079499fe7aca
Revises: ae68eccc1992
Create Date: 2025-05-12 14:46:56.232872

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "079499fe7aca"
down_revision: Union[str, None] = "ae68eccc1992"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column(
            "showcase_id", sa.Integer, sa.ForeignKey("showcases.id", ondelete="CASCADE")
        ),
        sa.Column("report_brief", sa.TEXT, nullable=False),
        sa.Column(
            "date_reported",
            sa.TIMESTAMP,
            nullable=False,
            server_default=sa.sql.func.now(),
        ),
        sa.Column("report_details", sa.TEXT),
    )


def downgrade() -> None:
    op.drop_table("reports")
