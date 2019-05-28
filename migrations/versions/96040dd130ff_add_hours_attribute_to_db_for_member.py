"""add hours attribute to db for member

Revision ID: 96040dd130ff
Revises: 33d0d35a5198
Create Date: 2019-05-20 22:54:52.336022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96040dd130ff'
down_revision = '33d0d35a5198'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('hours', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('member', 'hours')
    # ### end Alembic commands ###
