"""empty message

Revision ID: 18f625d3324c
Revises: 15fd7a6a74bd
Create Date: 2022-06-27 17:03:45.359127

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '18f625d3324c'
down_revision = '15fd7a6a74bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('royal_jelly', 'royesh_giah')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('royal_jelly', sa.Column('royesh_giah', mysql.VARCHAR(length=128), nullable=False))
    # ### end Alembic commands ###
