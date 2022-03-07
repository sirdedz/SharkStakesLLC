"""initial migration

Revision ID: 450680dac4e1
Revises: 
Create Date: 2022-03-07 23:36:06.949654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '450680dac4e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('listing', sa.Column('time', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('listing', 'time')
    # ### end Alembic commands ###
