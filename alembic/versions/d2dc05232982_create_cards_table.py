"""Create cards table

Revision ID: d2dc05232982
Revises: 
Create Date: 2021-11-30 13:23:26.817824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2dc05232982'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cards', sa.Column('card_id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('cards')
    pass
