"""Add created_at, active to cards

Revision ID: 7685fd00e696
Revises: 63f720ef6681
Create Date: 2021-11-30 15:18:55.453582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7685fd00e696'
down_revision = '63f720ef6681'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('cards', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))),
    op.add_column('cards', sa.Column('active', sa.Boolean(), nullable=False, server_default='TRUE'))
    pass


def downgrade():
    op.drop_column('cards', 'active')
    op.drop_column('cards', 'created_at')
    pass
