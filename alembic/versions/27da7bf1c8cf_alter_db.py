"""alter db

Revision ID: 27da7bf1c8cf
Revises: 29772ad7c274
Create Date: 2014-02-25 23:12:05.660592

"""

# revision identifiers, used by Alembic.
revision = '27da7bf1c8cf'
down_revision = '29772ad7c274'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roomcat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], name='fk_resource_id_roomcat', onupdate='cascade', ondelete='cascade', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hotelcat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], name='fk_resource_id_hotelcat', onupdate='cascade', ondelete='cascade', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_idx_users_username', 'user')
    op.create_index('unique_idx_users_username', 'user', [u'username'], unique=True)
    op.drop_constraint('unique_idx_users_email', 'user')
    op.create_index('unique_idx_users_email', 'user', [u'email'], unique=True)
    op.drop_constraint(None, 'resource_type')
    op.create_index('resource_type_name_key', 'resource_type', [u'name'], unique=True)
    op.drop_constraint('unique_idx_resource_type_name', 'resource_type')
    op.create_index('unique_idx_resource_type_name', 'resource_type', [u'name'], unique=True)
    op.drop_constraint('unique_idx_resource_type_module', 'resource_type')
    op.create_index('unique_idx_resource_type_module', 'resource_type', [u'module', u'resource_name'], unique=True)
    op.drop_constraint('unique_idx_currency_iso_code', 'currency')
    op.create_index('unique_idx_currency_iso_code', 'currency', [u'iso_code'], unique=True)
    op.alter_column(u'appointment_row', 'appointment_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_table('hotelcat')
    op.drop_table('roomcat')
    ### end Alembic commands ###
