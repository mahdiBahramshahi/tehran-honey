"""empty message

Revision ID: 052bba9cc976
Revises: 9f462a773f78
Create Date: 2022-06-12 09:38:04.383183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '052bba9cc976'
down_revision = '9f462a773f78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mahsolgroups', sa.Column('image_urlfor', sa.String(length=512), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mahsolgroups', 'image_urlfor')
    # ### end Alembic commands ###
