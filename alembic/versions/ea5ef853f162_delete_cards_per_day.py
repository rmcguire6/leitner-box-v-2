"""delete cards_per_day

Revision ID: ea5ef853f162
Revises: cb98a72750ab
Create Date: 2022-07-01 16:47:56.425572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea5ef853f162'
down_revision = 'cb98a72750ab'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'cards_per_day')
    pass


def downgrade():
    op.add_column('users', 'cards_per_day')
    pass
