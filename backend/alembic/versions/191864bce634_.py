"""empty message

Revision ID: 191864bce634
Revises: 762978ead34c
Create Date: 2021-11-17 13:59:41.387481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '191864bce634'
down_revision = '762978ead34c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('study', sa.Column('delayed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('study', 'delayed')
    # ### end Alembic commands ###
