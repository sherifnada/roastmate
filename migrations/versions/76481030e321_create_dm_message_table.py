"""Create dm_message table

Revision ID: 76481030e321
Revises: eb82aaa946fb
Create Date: 2023-09-17 22:37:57.656776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76481030e321'
down_revision: Union[str, None] = 'eb82aaa946fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dm_message",
        sa.Column("sender_number", sa.TEXT),
        sa.Column("with_number", sa.TEXT),
        sa.Column("date_sent", sa.TIMESTAMP(timezone=True)),
        sa.Column("date_received", sa.TIMESTAMP(timezone=True), index=True),
        sa.Column("content", sa.TEXT),
        sa.Column("sender_name", sa.TEXT),
        sa.Column("sender_role", sa.Enum("USER", "LLM", name="SenderRole")),
    )


def downgrade() -> None:
    op.drop_table("dm_message")
