"""initial

Revision ID: d7c8b23816b2
Revises: 930846208e16
Create Date: 2024-05-01 21:11:00.969954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7c8b23816b2'
down_revision: Union[str, None] = '930846208e16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the users table
    op.create_table('users',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column('username', sa.String(), unique=True, nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    )

    # Create the products table
    op.create_table('products',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    # Drop the products table
    op.drop_table('products')

    # Drop the users table
    op.drop_table('users')
