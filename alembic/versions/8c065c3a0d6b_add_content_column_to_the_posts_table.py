"""add content column to the posts table

Revision ID: 8c065c3a0d6b
Revises: 0b6aa04b01ea
Create Date: 2024-03-10 11:42:48.281894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c065c3a0d6b'
down_revision: Union[str, None] = '0b6aa04b01ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_column('posts', 'content')
    
    pass
