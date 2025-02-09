"""empty message

Revision ID: 1d0ba06f8dc4
Revises: 3d8172c987c7
Create Date: 2021-12-15 10:50:06.410130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d0ba06f8dc4'
down_revision = '3d8172c987c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('configuration',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('obligated_mode', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_configuration_id'), 'configuration', ['id'], unique=False)
    op.add_column('studystates', sa.Column('updated_by_id', sa.Integer(), nullable=True))
    op.drop_constraint('studystates_employee_id_fkey', 'studystates', type_='foreignkey')
    op.create_foreign_key(None, 'studystates', 'user', ['updated_by_id'], ['id'])
    op.drop_column('studystates', 'employee_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('studystates', sa.Column('employee_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'studystates', type_='foreignkey')
    op.create_foreign_key('studystates_employee_id_fkey', 'studystates', 'user', ['employee_id'], ['id'])
    op.drop_column('studystates', 'updated_by_id')
    op.drop_index(op.f('ix_configuration_id'), table_name='configuration')
    op.drop_table('configuration')
    # ### end Alembic commands ###
