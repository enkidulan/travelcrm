"""alter db

Revision ID: 29ebada6b768
Revises: 255a4fa72b25
Create Date: 2015-02-03 21:22:59.275697

"""

# revision identifiers, used by Alembic.
revision = '29ebada6b768'
down_revision = '255a4fa72b25'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lead',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lead_date', sa.Date(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('advsource_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['advsource_id'], ['advsource.id'], name='fk_advsource_id_lead', onupdate='cascade', ondelete='restrict'),
    sa.ForeignKeyConstraint(['customer_id'], ['person.id'], name='fk_customer_id_lead', onupdate='cascade', ondelete='restrict'),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], name='fk_resource_id_lead', onupdate='cascade', ondelete='restrict'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('apscheduler_jobs')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apscheduler_jobs',
    sa.Column('id', sa.VARCHAR(length=191), autoincrement=False, nullable=False),
    sa.Column('next_run_time', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('job_state', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=u'apscheduler_jobs_pkey')
    )
    op.drop_table('lead')
    ### end Alembic commands ###