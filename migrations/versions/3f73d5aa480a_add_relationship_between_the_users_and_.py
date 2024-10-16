"""add relationship between the users and books table

Revision ID: 3f73d5aa480a
Revises: 3ae2261d88db
Create Date: 2024-10-11 12:56:11.690397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '3f73d5aa480a'
down_revision: Union[str, None] = '3ae2261d88db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('user_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'books', 'users', ['user_id'], ['uid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'user_id')
    # ### end Alembic commands ###
