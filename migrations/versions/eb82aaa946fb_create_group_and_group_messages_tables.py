"""Create group and group_messages tables

Revision ID: eb82aaa946fb
Revises: 
Create Date: 2023-08-28 21:12:05.371469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb82aaa946fb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

fk_constraint = "fk_group_id"

def upgrade() -> None:
    op.create_table(
        "group",
        sa.column('id', sa.String(200), primary_key=True),
    )

    op.create_table(
        "group_message",
        sa.column("group_id", sa.String(200)),
        sa.column("date_sent", sa.TIMESTAMP(timezone=True)),
        sa.column("content", sa.Text()),
        sa.column("sender", sa.Text(20)),
    )

    op.create_foreign_key(
        name=fk_constraint,
        source_table="group_message",
        referent_table="group",
        local_cols=['group_id'],
        remote_cols=['id']
    )


def downgrade() -> None:
    op.drop_constraint(fk_constraint)
    op.drop_table("group_message")
    op.drop_table("group")
