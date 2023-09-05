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

pk_constraint = "pk_group_id"
fk_constraint = "fk_group_id"


def upgrade() -> None:
    op.create_table(
        "imessage_group",
        sa.Column('id', sa.String(200), primary_key=True),
    )

    op.create_table(
        "group_message",
        sa.Column("group_id", sa.String(200)),
        sa.Column("date_sent", sa.TIMESTAMP(timezone=True)),
        sa.Column("date_received", sa.TIMESTAMP(timezone=True), index=True),
        sa.Column("content", sa.TEXT),
        sa.Column("sender_number", sa.TEXT),
        sa.Column("sender_name", sa.TEXT),
        sa.Column("sender_role", sa.Enum("USER", "LLM", name="SenderRole")),
    )

    op.create_table(
        "contact",
        sa.Column("number", sa.TEXT, primary_key=True),
        sa.Column("name", sa.TEXT, nullable=True),
    )

    op.create_foreign_key(
        constraint_name=fk_constraint,
        source_table="group_message",
        local_cols=['group_id'],
        referent_table="imessage_group",
        remote_cols=['id'],
    )

    # op.create_foreign_key(
    #     constraint_name="contact_number_fk",
    #     source_table="group_message",
    #     local_cols=["sender_number"],
    #     referent_table="contact",
    #     remote_cols=["number"],
    # )

def downgrade() -> None:
    op.drop_constraint(fk_constraint, table_name="group_message")
    op.drop_constraint("contact_number_fk", table_name="group_message")

    op.drop_table("group_message")
    op.drop_table("imessage_group")
    op.drop_table("contact")

    op.execute('DROP TYPE "SenderRole";')
