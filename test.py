op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(50)),
        sa.Column('username', sa.String(100), nullable=False, unique=True),
        sa.Column('password', sa.String(100), nullable=False),
    )

# Create sale_receipts table
op.create_table('sale_receipts',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
    sa.Column('products', sa.String(300), nullable=False),
    sa.Column('payment_type', sa.String(50), nullable=False),
    sa.Column('payment_amount', sa.Float(), nullable=True),
    sa.Column('total_amount', sa.Float(), nullable=True),
    sa.Column('rest_amount', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
)

op.create_table(
    'token',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('user_id', sa.Integer),
    sa.Column('access_token', sa.String(450), primary_key=True),
    sa.Column('refresh_token', sa.String(450), nullable=False),
    sa.Column('status', sa.Boolean),
    sa.Column('created_date', sa.DateTime, default=sa.func.now()),
)