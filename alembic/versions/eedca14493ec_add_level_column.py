"""Add level column

Revision ID: eedca14493ec
Revises: d2dc05232982
Create Date: 2021-11-30 13:35:52.496359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eedca14493ec'
down_revision = 'd2dc05232982'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('cards', sa.Column('level', sa.Integer(), nullable=False, default = 1))
    pass


def downgrade():
    op.drop_column('cards','level')
    pass
