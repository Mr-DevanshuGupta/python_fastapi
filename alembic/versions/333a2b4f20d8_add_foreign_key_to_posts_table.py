"""add foreign key to posts table

Revision ID: 333a2b4f20d8
Revises: 98a2ed7d5ef8
Create Date: 2024-03-10 11:57:54.532546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '333a2b4f20d8'
down_revision: Union[str, None] = '98a2ed7d5ef8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),  nullable=False))
    op.create_foreign_key('posts_user_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

    pass


def downgrade():
    op.drop_constraint('posts_user_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    

    pass
