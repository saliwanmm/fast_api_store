"""initial

Revision ID: e0f5ef4c3507
Revises: 80c5fda4948a
Create Date: 2024-05-01 21:22:33.483445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0f5ef4c3507'
down_revision: Union[str, None] = '80c5fda4948a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the users table
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50)),
        sa.Column('username', sa.String(50), unique=True),
        sa.Column('password_hash', sa.String(), nullable=False),
    )

    # Create the products table
    op.create_table('products',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    )

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###