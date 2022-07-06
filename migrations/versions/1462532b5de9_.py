"""empty message

Revision ID: 1462532b5de9
Revises: 714cec12b84a
Create Date: 2022-06-23 11:39:17.951714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1462532b5de9'
down_revision = '714cec12b84a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('monasebat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('image', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('monasebat')
    # ### end Alembic commands ###
