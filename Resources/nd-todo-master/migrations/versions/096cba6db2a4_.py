"""empty message

Revision ID: 096cba6db2a4
Revises: 
Create Date: 2019-12-22 15:11:17.707850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '096cba6db2a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='todos_pkey')
    )
    # ### end Alembic commands ###
