"""Add foreign key to cards table

Revision ID: 63f720ef6681
Revises: c67dbfe55d47
Create Date: 2021-11-30 15:05:27.209215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63f720ef6681'
down_revision = 'c67dbfe55d47'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('cards', sa.Column('creator_id', sa.Integer(), nullable=False))
    op.create_foreign_key('cards_users_fk', source_table='cards', referent_table='users', local_cols=['creator_id'], remote_cols=['user_id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('cards_users_fk', table_name='cards')
    op.drop_column('cards', 'owner_id')
    pass
