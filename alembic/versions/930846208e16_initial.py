"""initial

Revision ID: 930846208e16
Revises: 300fa4a963b2
Create Date: 2024-05-01 20:47:07.903682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '930846208e16'
down_revision: Union[str, None] = '300fa4a963b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50)),
        sa.Column('price', sa.Integer),
    )


def downgrade() -> None:
    # Restore users table if needed
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50)),
        sa.Column('username', sa.String(50), unique=True),
        sa.Column('password', sa.String(50)),
    )
