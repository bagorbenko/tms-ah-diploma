"""third
Revision ID: 3e63d865f951
Revises: a8c8710d7389
Create Date: 2023-02-06 16:37:08.114580
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = '3e63d865f951'
down_revision = 'a8c8710d7389'
branch_labels = None
depends_on = None
def upgrade() -> None:
    op.drop_index('ix_purchase_book_id', table_name='purchase')
    op.drop_index('ix_purchase_id', table_name='purchase')
    op.drop_index('ix_purchase_user_id', table_name='purchase')
    op.drop_table('purchase')
def downgrade() -> None:
    op.create_table('purchase',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('book_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('book_title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('create_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('publisher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='purchase_pkey')
    )
    op.create_index('ix_purchase_user_id', 'purchase', ['user_id'], unique=False)
    op.create_index('ix_purchase_id', 'purchase', ['id'], unique=False)
    op.create_index('ix_purchase_book_id', 'purchase', ['book_id'], unique=False)
