"""empty message

Revision ID: 44b74a8548b5
Revises: 213e82e71a10
Create Date: 2022-06-11 15:02:28.062160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44b74a8548b5'
down_revision = '213e82e71a10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=256), nullable=False),
    sa.Column('upload_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('filename')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file')
    # ### end Alembic commands ###
