"""Add users table

Revision ID: c67dbfe55d47
Revises: eedca14493ec
Create Date: 2021-11-30 13:42:32.096803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c67dbfe55d47'
down_revision = 'eedca14493ec'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('user_id', sa.Integer, nullable=False),
    sa.Column('username', sa.String, nullable=False),
    sa.Column('email', sa.String, nullable=False),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('cards_per_day', sa.Integer, nullable=False, default=5),
    sa.Column('current_day_number', sa.Integer, nullable=False, default=1),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
