"""second
Revision ID: a8c8710d7389
Revises: 42bb9895dfe9
Create Date: 2023-02-05 21:09:28.248850
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = 'a8c8710d7389'
down_revision = '42bb9895dfe9'
branch_labels = None
depends_on = None
def upgrade() -> None:
    op.create_table('purchase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_title', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_book_id'), 'purchase', ['book_id'], unique=False)
    op.create_index(op.f('ix_purchase_id'), 'purchase', ['id'], unique=False)
    op.create_index(op.f('ix_purchase_user_id'), 'purchase', ['user_id'], unique=False)
    op.drop_table('roles')
def downgrade() -> None:
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey')
    )
    op.drop_index(op.f('ix_purchase_user_id'), table_name='purchase')
    op.drop_index(op.f('ix_purchase_id'), table_name='purchase')
    op.drop_index(op.f('ix_purchase_book_id'), table_name='purchase')
    op.drop_table('purchase')
