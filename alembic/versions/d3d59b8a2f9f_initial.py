"""initial

Revision ID: d3d59b8a2f9f
Revises: e519e0a2f6d6
Create Date: 2024-05-03 14:57:10.186017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3d59b8a2f9f'
down_revision: Union[str, None] = 'e519e0a2f6d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('access_token', sa.String(length=450), primary_key=True),
        sa.Column('refresh_token', sa.String(length=450), nullable=False),
        sa.Column('status', sa.Boolean(), nullable=True),
        sa.Column('created_date', sa.DateTime(), nullable=True, default=sa.func.now()),
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='products_pkey')
    )
    op.drop_table('token')
    # ### end Alembic commands ###
