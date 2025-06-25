"""initial
Revision ID: 42bb9895dfe9
Revises: 
Create Date: 2023-02-04 09:37:14.304628
"""
from alembic import op
import sqlalchemy as sa
revision = '42bb9895dfe9'
down_revision = None
branch_labels = None
depends_on = None
def upgrade() -> None:
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('permissions', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
def downgrade() -> None:
    op.drop_table('roles')
