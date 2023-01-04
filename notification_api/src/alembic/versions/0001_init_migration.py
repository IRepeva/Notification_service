"""init migration

Revision ID: 0001
Revises: 
Create Date: 2022-10-28 14:46:10.587855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event', sa.String(), nullable=True),
    sa.Column('is_instant', sa.BOOLEAN(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_templates_event'), 'templates', ['event'], unique=True)
    op.create_index(op.f('ix_templates_id'), 'templates', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_templates_id'), table_name='templates')
    op.drop_index(op.f('ix_templates_event'), table_name='templates')
    op.drop_table('templates')
    # ### end Alembic commands ###
