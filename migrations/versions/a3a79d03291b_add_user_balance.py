"""Add user balance

Revision ID: a3a79d03291b
Revises: 4d343adfa589
Create Date: 2022-03-13 14:45:36.083780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3a79d03291b'
down_revision = '4d343adfa589'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('balance', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'balance')
    # ### end Alembic commands ###
