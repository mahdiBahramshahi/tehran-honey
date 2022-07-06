"""empty message

Revision ID: 213e82e71a10
Revises: da26b43ea1c7
Create Date: 2022-06-11 12:49:22.805901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '213e82e71a10'
down_revision = 'da26b43ea1c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'mahsolat', ['title'])
    op.add_column('mahsolgroups', sa.Column('slug', sa.String(length=32), nullable=False))
    op.create_unique_constraint(None, 'mahsolgroups', ['title'])
    op.create_unique_constraint(None, 'mahsolgroups', ['slug'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mahsolgroups', type_='unique')
    op.drop_constraint(None, 'mahsolgroups', type_='unique')
    op.drop_column('mahsolgroups', 'slug')
    op.drop_constraint(None, 'mahsolat', type_='unique')
    # ### end Alembic commands ###
